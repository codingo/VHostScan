# VHostScan Wordlists Documentation

This document describes the wordlists available in VHostScan. This is an enhanced version of the original project by **Codingo** with additional improvements and expanded wordlists.

## Overview

VHostScan includes several specialized wordlists designed for different virtual host discovery scenarios. Each wordlist is optimized for specific use cases and environments.

## Available Wordlists

### 1. cloud-modern.txt (NEW)
**Size:** ~1,200 entries  
**Purpose:** Modern cloud services and container environments  
**Best for:** AWS, Azure, GCP, Docker, Kubernetes environments

**Contains:**
- Cloud service subdomains (api, cdn, static, assets)
- Container orchestration endpoints
- Modern web architecture patterns
- Microservices naming conventions

**Example usage:**
```bash
python VHostScan.py -t example.com -w wordlists/cloud-modern.txt
```

### 2. common-vhosts.txt (ENHANCED)
**Size:** ~800 entries  
**Purpose:** Most common virtual host patterns  
**Best for:** General purpose scanning, initial reconnaissance

**Contains:**
- Standard subdomain patterns (www, mail, ftp, admin)
- Common service endpoints
- Legacy and modern naming conventions
- International variations

**Example usage:**
```bash
python VHostScan.py -t example.com -w wordlists/common-vhosts.txt
```

### 3. pentest-focused.txt (NEW)
**Size:** ~600 entries  
**Purpose:** Penetration testing and security assessments  
**Best for:** Security professionals, bug bounty hunters

**Contains:**
- Security-related endpoints
- Admin interfaces and panels
- Development and staging environments
- Testing and debugging interfaces

**Example usage:**
```bash
python VHostScan.py -t example.com -w wordlists/pentest-focused.txt
```

### 4. virtual-host-scanning.txt (ORIGINAL)
**Size:** ~1,000+ entries  
**Purpose:** Comprehensive virtual host discovery  
**Best for:** Thorough enumeration

**Contains:**
- Extensive subdomain list
- Various naming patterns
- Legacy system endpoints

### 5. simple.txt (ORIGINAL)
**Size:** ~100 entries  
**Purpose:** Quick basic scanning  
**Best for:** Fast initial checks

### 6. testing.txt (ORIGINAL)
**Size:** ~20 entries  
**Purpose:** Development and testing  
**Best for:** Local development, proof of concept

### 7. hackthebox.txt (ORIGINAL)
**Size:** ~50 entries  
**Purpose:** CTF and HackTheBox challenges  
**Best for:** Educational purposes, CTF competitions

## Usage Recommendations

### For Different Scenarios:

**Quick Assessment:**
```bash
python VHostScan.py -t target.com -w wordlists/simple.txt
```

**General Purpose Scan:**
```bash
python VHostScan.py -t target.com -w wordlists/common-vhosts.txt
```

**Cloud Environment:**
```bash
python VHostScan.py -t target.com -w wordlists/cloud-modern.txt
```

**Security Assessment:**
```bash
python VHostScan.py -t target.com -w wordlists/pentest-focused.txt
```

**Comprehensive Scan:**
```bash
python VHostScan.py -t target.com -w wordlists/virtual-host-scanning.txt
```

### Combining Wordlists:

You can combine multiple wordlists for comprehensive coverage:

```bash
# Combine common and cloud wordlists
cat wordlists/common-vhosts.txt wordlists/cloud-modern.txt > combined.txt
python VHostScan.py -t target.com -w combined.txt
```

## Wordlist Quality and Sources

### Original Wordlists (by Codingo)
- Based on real-world penetration testing experience
- Curated from security assessments and bug bounty hunting
- Regularly updated based on community feedback

### Enhanced Wordlists (Improvements)
- **cloud-modern.txt**: Based on modern cloud infrastructure patterns
- **pentest-focused.txt**: Specialized for security assessments
- **common-vhosts.txt**: Enhanced with additional common patterns

### Quality Assurance
- All wordlists are deduplicated
- Entries are validated for common patterns
- Regular updates based on emerging technologies

## Performance Considerations

| Wordlist | Entries | Scan Time* | Memory Usage |
|----------|---------|------------|--------------|
| simple.txt | ~100 | < 1 min | Low |
| testing.txt | ~20 | < 30 sec | Very Low |
| common-vhosts.txt | ~800 | 2-5 min | Medium |
| pentest-focused.txt | ~600 | 2-4 min | Medium |
| cloud-modern.txt | ~1,200 | 3-6 min | Medium |
| virtual-host-scanning.txt | ~1,000+ | 5-10 min | High |

*Estimated scan times for typical targets with default settings

## Custom Wordlists

You can create custom wordlists by:

1. Creating a text file with one entry per line
2. Using the format: `subdomain` (without the domain)
3. Saving with `.txt` extension in the wordlists directory

**Example custom wordlist:**
```
myapp
staging-api
dev-portal
internal-admin
```

## Contributing

To contribute new wordlists or improve existing ones:

1. Fork the repository
2. Add your wordlist to the `VHostScan/wordlists/` directory
3. Update this documentation
4. Submit a pull request

### Wordlist Guidelines:
- One entry per line
- No duplicate entries
- No comments or special characters
- Use lowercase for consistency
- Focus on real-world scenarios

## Credits

- **Original Project:** [Codingo](https://github.com/codingo) - VHostScan creator
- **Enhancements:** Additional wordlists and improvements by the community
- **Sources:** Real-world penetration testing, bug bounty research, cloud infrastructure patterns

---

*This is an enhanced version of VHostScan by Codingo with additional improvements and expanded wordlists for better virtual host discovery.*
