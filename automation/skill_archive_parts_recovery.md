# Missing Archive Parts Recovery Guide
**Created**: 2026-01-25  
**Purpose**: Track and recover missing parts for incomplete multi-part archives

---

## Current Missing Files

### Priority 1: Large Files in Archives Folder

#### 1. Wet_Food_6.part1.rar (10 GB)
- **Location**: `C:\Users\sol90\Downloads\Archives\`
- **Missing**: part2.rar
- **Status**: Incomplete
- **Action**: Search browser history or re-download from source

#### 2. University.CoEds.33.part1.rar (400 MB)
- **Location**: `C:\Users\sol90\Downloads\Archives\`
- **Missing**: part2.rar
- **Status**: Incomplete
- **Action**: Search browser history or re-download from source

### Priority 2: Files in Downloads Root

#### 3. 74.Mag.Club.Special.Editions.part2.rar (2.1 GB)
- **Location**: `C:\Users\sol90\Downloads\`
- **Missing**: part1.rar
- **Status**: Incomplete (only have part 2)
- **Action**: Search browser history or re-download part1

#### 4. One_Night_In_Paris.part2.rar (2.4 GB)
- **Location**: `C:\Users\sol90\Downloads\`
- **Missing**: part1.rar
- **Status**: Incomplete (only have part 2)
- **Action**: Search browser history or re-download part1

#### 5. Bush_Administration.z01 (350 MB)
- **Location**: `C:\Users\sol90\Downloads\`
- **Missing**: Bush_Administration.zip (main file)
- **Status**: Incomplete (only have .z01 part)
- **Action**: Search browser history or re-download main zip file

### Already Cleaned (Deleted)

These were deleted during the 2026-01-25 audit:
- ✓ Barely_Legal_57.zip (missing .z01)
- ✓ Barely_Legal_71.zip (missing .z01)
- ✓ Barely_Legal_Bikini_Blondes_2.zip (missing .z01)

---

## Recovery Methods

### Method 1: Browser History Search (Recommended)

**Using the Search Script**:
```powershell
& "G:\My Drive\04_Resources\Tools\Scripts\PowerShell\search_browser_history.ps1"
```

**Manual Browser Search**:
1. Open browser history (Ctrl+H)
2. Search for file names:
   - "wet food"
   - "university coed"
   - "club special editions"
   - "one night paris"
   - "bush administration"
3. Look for download URLs from the past 30-60 days
4. Revisit the source and download missing parts

### Method 2: DB Browser for SQLite

**Chrome History**:
```
C:\Users\sol90\AppData\Local\Google\Chrome\User Data\Default\History
```

**Edge History**:
```
C:\Users\sol90\AppData\Local\Microsoft\Edge\User Data\Default\History
```

**Steps**:
1. Download DB Browser for SQLite: https://sqlitebrowser.org/
2. Close your browser (to unlock the database)
3. Open the History file in DB Browser
4. Browse the `urls` table
5. Search for download URLs containing file names
6. Copy URLs and re-download missing parts

### Method 3: Check Download Manager History

If you use a download manager (e.g., Internet Download Manager, Free Download Manager):
1. Open the download manager
2. Check download history
3. Look for the archive file names
4. Re-download from the same source

### Method 4: Check Torrent Client

If downloaded via torrent:
1. Open your torrent client (Deluge, qBittorrent, etc.)
2. Check completed/removed torrents list
3. Re-add the torrent to download missing parts
4. Or search for the torrent again on the original tracker

---

## Decision Matrix

For each incomplete archive, decide:

### Option A: Recover Missing Parts
- **If**: You can find the download source
- **Action**: Download missing parts and extract
- **Time**: 15-60 minutes per archive
- **Benefit**: Recover the content

### Option B: Delete Incomplete Archives
- **If**: Cannot find source OR content not needed
- **Action**: Delete to free up ~15 GB of space
- **Time**: 2 minutes
- **Benefit**: Clean up Downloads folder

---

## Recommended Actions by File

| File | Size | Recommendation | Reason |
|------|------|----------------|--------|
| Wet_Food_6.part1.rar | 10 GB | **DELETE** | Very large, takes up most space |
| University.CoEds.33.part1.rar | 400 MB | Try to recover | Smaller, easier to re-download |
| 74.Mag.Club.Special.Editions.part2.rar | 2.1 GB | Try to recover | Magazine collection, may be valuable |
| One_Night_In_Paris.part2.rar | 2.4 GB | **DELETE** | Likely available elsewhere |
| Bush_Administration.z01 | 350 MB | Try to recover | Smaller file |

**Total space to free if all deleted**: ~15 GB

---

## Quick Cleanup Script

If you decide to delete all incomplete archives:

```powershell
# Delete all incomplete multi-part archives
Remove-Item "C:\Users\sol90\Downloads\Archives\University.CoEds.33.part1.rar" -Force
Remove-Item "C:\Users\sol90\Downloads\Archives\Wet_Food_6.part1.rar" -Force
Remove-Item "C:\Users\sol90\Downloads\74.Mag.Club.Special.Editions.part2.rar" -Force
Remove-Item "C:\Users\sol90\Downloads\One_Night_In_Paris.part2.rar" -Force
Remove-Item "C:\Users\sol90\Downloads\Bush_Administration.z01" -Force

Write-Host "Deleted incomplete archives - freed ~15 GB"
```

---

## Prevention for Future

To avoid incomplete downloads in the future:

1. **Check file count before downloading**: Multi-part archives show "Part 1 of 3" etc.
2. **Download all parts together**: Don't start extraction until all parts are present
3. **Use download manager**: Helps track multi-part downloads
4. **Keep download links**: Save URLs in a text file until extraction is complete
5. **Verify before deleting source**: Always test extraction before removing archives

---

## Status Tracking

Update this section as you recover or delete files:

- [ ] Wet_Food_6.part1.rar - Decision: ___________
- [ ] University.CoEds.33.part1.rar - Decision: ___________
- [ ] 74.Mag.Club.Special.Editions.part2.rar - Decision: ___________
- [ ] One_Night_In_Paris.part2.rar - Decision: ___________
- [ ] Bush_Administration.z01 - Decision: ___________

**Last Updated**: 2026-01-25
