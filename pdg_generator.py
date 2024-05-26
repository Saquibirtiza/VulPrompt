import os

dirs = ["Vul", "No-Vul"]
source_dir = "./reveal_source/"
output_dir = "./reveal_bin/"
pdgs_dir = "./reveal_pdgs/"
joern_path = "./joern-cli"

for dir in dirs:
  input_path = source_dir + dir + "/"
  if os.path.exists(input_path):
    for files in os.listdir(input_path):
      filename = files.split(".")[0]
      if dir == "Vul":
        inp = input_path + filename + ".c"
        if not os.path.exists(output_dir + "Vul/"):
          os.makedirs(output_dir + "Vul/")  
        if not os.path.exists(pdgs_dir + "Vul/"):
          os.makedirs(pdgs_dir + "Vul/")  
        out = output_dir + "Vul/" + filename + '.bin'
        pdgs = pdgs_dir + "Vul/" + filename
      else:
        inp = input_path + filename + ".c"
        if not os.path.exists(output_dir + "No-Vul/"):
          os.makedirs(output_dir + "No-Vul/")  
        if not os.path.exists(pdgs_dir + "No-Vul/"):
          os.makedirs(pdgs_dir + "No-Vul/")  
        out = output_dir + "No-Vul/" + filename + '.bin'
        pdgs = pdgs_dir + "No-Vul/" + filename

      os.environ['file'] = str(inp)
      os.environ['out'] = str(out) 
      os.system('sh ' + joern_path + '/joern-parse $file --language c -o $out')

      os.environ['bin'] = str(out)
      os.environ['pdgs'] = str(pdgs)
      os.system('sh ' + joern_path + '/joern-export $bin'+ " --repr " + "pdg" + ' -o $pdgs') 

      pdg_list = os.listdir(pdgs)
      for pdg in pdg_list:
        if pdg.startswith("1-pdg"):
          file_path = os.path.join(pdgs, pdg)
          with open(file_path, 'r') as f:
            content = f.readlines()
            if "&lt;global&gt" in content[0]:
              print("Dot file deleted because empty!")
              os.system("rm -rf "+pdgs)
              break
          os.system("mv "+file_path+' '+pdgs+'.dot')
          os.system("rm -rf "+pdgs)
          break
 
# Closing file
f.close()