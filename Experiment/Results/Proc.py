import sys

def values_per_bitrate(bitrate,typeof,content):
    write = open("values_for_mos_per_bitrate_and_type/bitrate{0}_type_{1}_content_{2}.txt".format(bitrate,typeof,content), "w") 
    for i in range(1,10):
        read = open("answers_0{0}.txt".format(i),"r") 
        for line in read:
            if "{0}_geom0{1}_text0{1}_octree-{2}".format(content,bitrate,typeof)in line: 
                write.write(line.split()[2] + "\n")
        read.close()
    write.close()

def main():
    contents = ['loot_vox10_1200_vox10_dec','biplane_vox10_dec','amphoriskos_vox10_dec','longdress_vox10_1300_dec']
    typesof=['raht','predlift']
    bitrates = [2,3,4,5,6]
    for elem1 in typesof:
        for elem2 in bitrates:
            for elem3 in contents:
                values_per_bitrate(elem2,elem1,elem3)
                
if __name__=="__main__":
    main()
            

