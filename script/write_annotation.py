# -*- coding:utf-8 -*-  

import xml.etree.ElementTree as ET



def write_annotation(file_name,position):
	class_dict={0:"peason",1:'head',2:'uppperbody',3:"leg"}
	root = ET.Element('voc')
	tree = ET.ElementTree(root)

	for i in range(4):
		obj = ET.Element('object')
		root.append(obj)

		name = ET.Element('name')
		name.text=class_dict[i]
		# 'test'
		obj.append(name)

		pose = ET.Element('pose')
		pose.text='1'
		obj.append(pose)

		truncated = ET.Element('truncated')
		truncated.text='0'
		obj.append(truncated)


		difficult = ET.Element('difficult')
		difficult.text='0'
		obj.append(difficult)

		bndbox = ET.Element('bndbox')
		obj.append(bndbox)

		xmin=ET.Element('xmin')
		xmin.text=str(position[4*i])
		bndbox.append(xmin)

		ymin=ET.Element('ymin')
		ymin.text=str(position[4*i+1])
		bndbox.append(ymin)


		xmax=ET.Element('xmax')
		xmax.text=str(int(position[4*i])+int(position[4*i+2]))
		bndbox.append(xmax)

		ymax=ET.Element('ymax')
		ymax.text=str(int(position[4*i])+int(position[4*i+3]))
		bndbox.append(ymax)
	try:
		tree.write(file_name)

	except BaseException,e:
		print e
		pass
	return tree


# import xml.dom.minidom as MD
	# ,'utf8')