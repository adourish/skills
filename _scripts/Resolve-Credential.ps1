# Resolve-Credential.ps1
# Cascade credential lookup across pskills -> aitools -> skills.
# Reads ~/.credentials/config.json for provider order and aliases.
#
# Usage:
#   $token = Resolve-Credential -Name "todoist" -Field "api.apiToken"
#   $creds = Resolve-Credential -Name "dmedev5"

param(
    [Parameter(Mandatory=$true)]
    [string]$Name,

    [Parameter(Mandatory=$false)]
    [string]$Field = ""
)

$configPath = Join-Path $env:USERPROFILE ".credentials\config.json"
if (-not (Test-Path $configPath)) {
    throw "Resolver config not found: $configPath"
}

$config = Get-Content $configPath | ConvertFrom-Json

$keyPath = $config.decryption_key_path
if (-not (Test-Path $keyPath)) {
    throw "DevKey not found: $keyPath"
}
$keyBase64 = Get-Content $keyPath
$key = [Convert]::FromBase64String($keyBase64)

# Resolve alias -> canonical name
$canonical = $Name
if ($config.aliases.PSObject.Properties[$Name]) {
    $canonical = $config.aliases.$Name
}

function Unprotect-Field {
    param([string]$EncValue)
    if (-not $EncValue.StartsWith("ENC:")) { return $EncValue }
    $data = [Convert]::FromBase64String($EncValue.Substring(4))
    $iv   = $data[0..15]
    $ct   = $data[16..($data.Length - 1)]
    $aes  = [System.Security.Cryptography.Aes]::Create()
    $aes.Key = $key
    $aes.IV  = $iv
    $dec  = $aes.CreateDecryptor()
    $plain = $dec.TransformFinalBlock($ct, 0, $ct.Length)
    $dec.Dispose(); $aes.Dispose()
    return [System.Text.Encoding]::UTF8.GetString($plain)
}

function Decrypt-Object {
    param($obj)
    if ($obj -is [string]) {
        return Unprotect-Field $obj
    }
    if ($obj -is [PSCustomObject]) {
        $result = [PSCustomObject]@{}
        foreach ($prop in $obj.PSObject.Properties) {
            $result | Add-Member -NotePropertyName $prop.Name -NotePropertyValue (Decrypt-Object $prop.Value)
        }
        return $result
    }
    return $obj
}

function Dig-Field {
    param($obj, [string]$path)
    foreach ($part in $path.Split('.')) {
        if ($null -eq $obj -or -not $obj.PSObject.Properties[$part]) {
            throw "Field '$path' not found in credentials"
        }
        $obj = $obj.$part
    }
    return $obj
}

# Search providers in order, skip any whose path doesn't exist
foreach ($provider in $config.search_paths) {
    $keysPath = $provider.keys_path
    if (-not (Test-Path $keysPath)) {
        Write-Verbose "Skipping provider '$($provider.name)': path not found"
        continue
    }

    $keyFile = Join-Path $keysPath "$($canonical.ToLower())-keys.json"
    if (Test-Path $keyFile) {
        Write-Verbose "Resolved '$Name' via provider '$($provider.name)'"
        $data   = Get-Content $keyFile | ConvertFrom-Json
        $creds  = Decrypt-Object $data.encryptedCredentials

        if ($Field) {
            return Dig-Field $creds $Field
        }
        return $creds
    }
}

throw "Credential '$Name' (canonical: '$canonical') not found in any provider"
