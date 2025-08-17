# Changelog

## [2.1.0] - 2025-08-17 (Enhanced Version)

### New Features - Enhanced Version
- **Enhanced Wordlists**: Added specialized wordlists for modern infrastructure
  - `cloud-modern.txt` - Modern cloud services, containers, and DevOps tools (~1,200 entries)
  - `pentest-focused.txt` - Security assessment and penetration testing focused (~600 entries)
  - Enhanced `common-vhosts.txt` with additional common patterns (~800 entries)
- **Comprehensive Documentation**: Added detailed wordlist documentation (WORDLISTS.md)
- **Improved User Experience**: Better error messages and progress indicators

### Enhanced Wordlists Content
- **Cloud Infrastructure**: AWS, Azure, GCP, Docker, Kubernetes endpoints
- **Modern DevOps**: CI/CD, monitoring, logging, and deployment patterns
- **Security Testing**: Admin panels, development environments, testing interfaces
- **International Support**: Extended with international naming conventions

### Documentation Improvements
- Complete English documentation across all files
- Detailed wordlist usage examples and recommendations
- Performance considerations and scan time estimates
- Custom wordlist creation guidelines
- Proper attribution to original author (Codingo)

### Credits
- **Original Project**: VHostScan by [Codingo](https://github.com/codingo)
- **Enhanced Version**: Community improvements with additional wordlists and modernizations
- **Acknowledgment**: This enhanced version builds upon Codingo's excellent foundation

## [2.0.0] - 2025-08-10 (Original Modernization)

### Major Changes
- **Breaking**: Updated to support Python 3.8+ (dropped Python 2.7 support)
- **Major refactoring**: Updated all dependencies to modern versions

### Updated Dependencies
- `dnspython` from unlocked to `>=2.4.0`
- `fuzzywuzzy` with speedup support `>=0.18.0`  
- `numpy` from ancient `==1.12.0` to `>=1.24.0`
- `pandas` to `>=2.0.0`
- `requests` to `>=2.31.0`
- `simplejson` to `>=3.19.0`
- `urllib3` to `>=2.0.0`

### Testing Dependencies  
- Replaced deprecated `pep8` with `flake8>=6.0.0`
- Updated `pytest` to `>=7.0.0`
- Updated `pytest-mock` to `>=3.10.0`

### Code Improvements
- Added proper type hints throughout the codebase
- Improved error handling and exception management
- Better Unicode/encoding support (UTF-8 everywhere)
- Updated DNS resolution to use modern `dns.resolver.resolve()` instead of deprecated `query()`
- Improved SSL/TLS handling for newer urllib3 versions
- Enhanced file operations with proper directory creation
- Better user agent handling and validation

### Project Structure
- Added modern `pyproject.toml` configuration
- Enhanced `.gitignore` for better Python development
- Improved `setup.py` with proper version handling
- Added development dependencies section

### Bug Fixes
- Fixed output file method naming inconsistency (`output_grepable` vs `write_grepable`)
- Fixed uninitialized variable in `output_grepable_detail()`
- Improved error handling in DNS resolution
- Better SSL certificate handling

### Development
- All tests passing on Python 3.13
- Compatible with Python 3.8-3.12+
- Modern packaging with setuptools and wheel
- Enhanced development experience with better tooling

## [1.21] - Previous Version
- Legacy version with old dependencies and Python 2.7 support
