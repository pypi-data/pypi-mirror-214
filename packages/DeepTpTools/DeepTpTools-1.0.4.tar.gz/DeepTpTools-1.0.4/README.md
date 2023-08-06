# DeepTpTools
Protein prediction package


## Environmental installation
### Model Download
You can download the model in the following two ways:
1. https://drive.google.com/drive/folders/1OEKabeJmdGiGG1PJsPu0bgcE5_GVGXc9?usp=share_link
2. https://luke9012.lanzoub.com/b00r1vhre | password:ddpt

After the download is completed, pass in the folder path
`p = DeepTp(r'D:\_code\_github\DeepTpTools\drop')`

### R
R language version requires version 4.1.3 or higher
Two packages need to be installed simultaneously:
```
install.packages("protr")
install.packages("DT")
```
Set Simultaneously`R_HOME`to environment variable

### Python
Python version requires`3.6`or higher


## How to use
### If there is a protein sequence
```python
name = "Q4JB77"
seq = "MRAAVLEEYKKPLRISEVDSPSINESSEVLLQVTATGLCHGDIHIAMGEWDSQIQVNLPIILGHEVVGRVLQSNHDKIKKNDLVLVYNAFGCKNCKYCKFKEYQFCEKVKVIGVNLNGGFAEYVKIPDGDNLVRVNTSDPIKLAPLADAGLTAYNSVKDLEENSKVLIIGTGAVALIALQLLKLKNVDVTVIGENQLKLDSAEKLGADEVISIKREEDSYLSLLPGKKFDYILDYVGSTRTLAESPWLLNKKGELRIIGEFGGVLRAEEQLLVLRGLRIRGILYGSLQDLKHILDIYLKGKIDTLTTVYKLEDINEAITDVTEGKVVGRAVIVP"
p = DeepTp(r'D:\_code\_github\ProTstab2\drop')
r, r2 = p.predict(name, seq)
print(r, r2)
# 0.8722285 Thermophilic protein
```
### If there is no protein sequence, the following methods can be used
Method 1：
```python
name = "Q4JB77"
p = DeepTp(r'D:\_code\_github\ProTstab2\drop')
seq = p.get_seq_info(name)
r, r2 = p.predict(name, seq)
print(r, r2)
# 0.8722285 Thermophilic protein
```
Method 2：
```python
name = "Q4JB77"
p = DeepTp(r'D:\_code\_github\ProTstab2\drop')
r, r2 = p.predict(name)
print(r, r2)
# 0.8722285 Thermophilic protein
```
The first method is recommended here for the following reasons：
1. Due to the use of crawlers, it is not guaranteed that data can be obtained every time, and the program may crash
2. You can obtain specific protein sequence values

## Disclaimers
The applications involved in this package are for learning and communication purposes only and shall not be used for any commercial purposes. 
Any legal disputes arising from this have nothing to do with me!