# SkillzUtils

## Installation
Download repository as zip and then run:
```bash
python3 setup.py install
```
in the appropriate directory.

## Setup
To setup with IDM connection
```bash
SkillzUtil config [User] [Password] [Tournament_index] --connection_type idm
```

To setup with a local connection (not recommended)
```bash
SkillzUtil config [eMail] [Password] [Tournament_index] --connection_type local
```

## Usage examples
Running games against top 25
```bash
SkillzUtil run-games sample 25 --selector top --log ~/top25.csv
```
(A log will be dumped to ~/top25.csv)
<br/>
Running games against random 10 opponents
```bash
SkillzUtil run-games sample 25 --selector random --log ~/random25.csv
```
(A log will be dumped to ~/random25.csv)