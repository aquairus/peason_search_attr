import os 

# todo=[ "mkdir Annotations","mkdir  ImageSets/Main" ,"mv RAP_dataset JPEGImages"
# ]
# for thing in todo:
# 	try:
# 		os.system(thing)
# 	except BaseException,e:
# 		pass

from rap_db import RAP
from write_annotation import write_annotation
db_path="/Users/apple/desktop/RAP"
db = RAP(db_path, 0)

f=open("ImageSets/Main/trainval.txt","w+")
for i in db.train_ind:
	try:
		# f.write(str(i)+"\n")
		# old_name=db.get_img_path(i).split("RAP/")[1]
		position=db.position[i]
		# print old_name
		# os.rename(old_name,"JPEGImages/"+str(i)+".png")
		b=write_annotation('Annotations/'+str(i)+".xml",position)

	except BaseException,e:
		print e
		pass




# os.system("mv RAP_dataset JPEGImages")