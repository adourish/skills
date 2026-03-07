# Salesforce Metadata Sync Script
# Generic version - no organization-specific names
# 
# Usage:
#   .\sfsync.ps1 -type apex -pattern "MyClass*" -action push -org myorg
#   .\sfsync.ps1 -type lwc -pattern "myComponent" -action pull -org myorg
#   .\sfsync.ps1 -type object -pattern "MyObject__c" -action push -org myorg
#   .\sfsync.ps1 -type all -action push -org myorg

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet('apex', 'lwc', 'aura', 'object', 'trigger', 'vf', 'all')]
    [string]$type,
    
    [Parameter(Mandatory=$false)]
    [string]$pattern = "*",
    
    [Parameter(Mandatory=$true)]
    [ValidateSet('push', 'pull')]
    [string]$action,
    
    [Parameter(Mandatory=$true)]
    [string]$org
)

# Color output functions
function Write-Success {
    param([string]$message)
    Write-Host $message -ForegroundColor Green
}

function Write-Info {
    param([string]$message)
    Write-Host $message -ForegroundColor Cyan
}

function Write-Warning {
    param([string]$message)
    Write-Host $message -ForegroundColor Yellow
}

function Write-Error {
    param([string]$message)
    Write-Host $message -ForegroundColor Red
}

# Metadata type mappings
$metadataTypes = @{
    'apex' = @{
        'path' = 'force-app/main/default/classes'
        'extension' = '.cls'
        'metadataType' = 'ApexClass'
    }
    'lwc' = @{
        'path' = 'force-app/main/default/lwc'
        'extension' = ''
        'metadataType' = 'LightningComponentBundle'
    }
    'aura' = @{
        'path' = 'force-app/main/default/aura'
        'extension' = ''
        'metadataType' = 'AuraDefinitionBundle'
    }
    'object' = @{
        'path' = 'force-app/main/default/objects'
        'extension' = ''
        'metadataType' = 'CustomObject'
    }
    'trigger' = @{
        'path' = 'force-app/main/default/triggers'
        'extension' = '.trigger'
        'metadataType' = 'ApexTrigger'
    }
    'vf' = @{
        'path' = 'force-app/main/default/pages'
        'extension' = '.page'
        'metadataType' = 'ApexPage'
    }
}

# Main execution
Write-Info "========================================="
Write-Info "Salesforce Metadata Sync"
Write-Info "========================================="
Write-Info "Type: $type"
Write-Info "Pattern: $pattern"
Write-Info "Action: $action"
Write-Info "Org: $org"
Write-Info "========================================="

try {
    if ($type -eq 'all') {
        # Deploy all metadata
        Write-Info "Deploying all metadata..."
        
        if ($action -eq 'push') {
            $result = sfdx force:source:deploy -p "force-app/main/default" -u $org 2>&1
        } else {
            $result = sfdx force:source:retrieve -p "force-app/main/default" -u $org 2>&1
        }
        
        if ($LASTEXITCODE -eq 0) {
            Write-Success "✓ Successfully $action all metadata"
        } else {
            Write-Error "✗ Failed to $action metadata"
            Write-Error $result
            exit 1
        }
    } else {
        # Get metadata configuration
        $config = $metadataTypes[$type]
        $basePath = $config.path
        
        # Find matching items
        Write-Info "Searching for $type matching pattern: $pattern"
        
        if ($type -eq 'apex' -or $type -eq 'trigger' -or $type -eq 'vf') {
            # File-based metadata
            $searchPath = Join-Path $basePath "$pattern$($config.extension)"
            $items = Get-ChildItem -Path $searchPath -ErrorAction SilentlyContinue
            
            if ($items) {
                Write-Info "Found $($items.Count) item(s)"
                
                foreach ($item in $items) {
                    Write-Info "  - $($item.Name)"
                }
                
                # Build deployment path
                $deployPaths = $items | ForEach-Object { $_.FullName }
                $deployPathString = $deployPaths -join ','
                
                if ($action -eq 'push') {
                    Write-Info "Deploying to $org..."
                    $result = sfdx force:source:deploy -p $deployPathString -u $org 2>&1
                } else {
                    Write-Info "Retrieving from $org..."
                    $result = sfdx force:source:retrieve -p $deployPathString -u $org 2>&1
                }
                
                if ($LASTEXITCODE -eq 0) {
                    Write-Success "✓ Successfully $action $($items.Count) item(s)"
                } else {
                    Write-Error "✗ Failed to $action items"
                    Write-Error $result
                    exit 1
                }
            } else {
                Write-Warning "No items found matching pattern: $pattern"
                exit 1
            }
        } elseif ($type -eq 'lwc' -or $type -eq 'aura') {
            # Directory-based metadata (components)
            $searchPath = Join-Path $basePath $pattern
            $items = Get-ChildItem -Path $searchPath -Directory -ErrorAction SilentlyContinue
            
            if ($items) {
                Write-Info "Found $($items.Count) component(s)"
                
                foreach ($item in $items) {
                    Write-Info "  - $($item.Name)"
                }
                
                # Build deployment path
                $deployPaths = $items | ForEach-Object { $_.FullName }
                $deployPathString = $deployPaths -join ','
                
                if ($action -eq 'push') {
                    Write-Info "Deploying to $org..."
                    $result = sfdx force:source:deploy -p $deployPathString -u $org 2>&1
                } else {
                    Write-Info "Retrieving from $org..."
                    $result = sfdx force:source:retrieve -p $deployPathString -u $org 2>&1
                }
                
                if ($LASTEXITCODE -eq 0) {
                    Write-Success "✓ Successfully $action $($items.Count) component(s)"
                } else {
                    Write-Error "✗ Failed to $action components"
                    Write-Error $result
                    exit 1
                }
            } else {
                Write-Warning "No components found matching pattern: $pattern"
                exit 1
            }
        } elseif ($type -eq 'object') {
            # Object metadata
            $searchPath = Join-Path $basePath $pattern
            $items = Get-ChildItem -Path $searchPath -Directory -ErrorAction SilentlyContinue
            
            if ($items) {
                Write-Info "Found $($items.Count) object(s)"
                
                foreach ($item in $items) {
                    Write-Info "  - $($item.Name)"
                }
                
                # Build deployment path
                $deployPaths = $items | ForEach-Object { $_.FullName }
                $deployPathString = $deployPaths -join ','
                
                if ($action -eq 'push') {
                    Write-Info "Deploying to $org..."
                    $result = sfdx force:source:deploy -p $deployPathString -u $org 2>&1
                } else {
                    Write-Info "Retrieving from $org..."
                    $result = sfdx force:source:retrieve -p $deployPathString -u $org 2>&1
                }
                
                if ($LASTEXITCODE -eq 0) {
                    Write-Success "✓ Successfully $action $($items.Count) object(s)"
                } else {
                    Write-Error "✗ Failed to $action objects"
                    Write-Error $result
                    exit 1
                }
            } else {
                Write-Warning "No objects found matching pattern: $pattern"
                exit 1
            }
        }
    }
    
    Write-Info "========================================="
    Write-Success "Sync completed successfully!"
    Write-Info "========================================="
    
} catch {
    Write-Error "An error occurred: $_"
    exit 1
}
