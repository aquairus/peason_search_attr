# USAGE
# python search.py --index index.csv --query queries/103100.png --result-path dataset

# import the necessary packages
from lib.pyimagesearch.colordescriptor import ColorDescriptor
from lib.pyimagesearch.searcher import Searcher
import argparse
import cv2

# construct the argument parser and parse the arguments
# ap = argparse.ArgumentParser()
# ap.add_argument("-i", "--index", required = True,
# 	help = "Path to where the computed index will be stored")
# ap.add_argument("-q", "--query", required = True,
# 	help = "Path to the query image")
# ap.add_argument("-r", "--result-path", required = True,
# 	help = "Path to the result path")
# args = vars(ap.parse_args())

# initialize the image descriptor
def image_search(query_image,index='data/index.csv',result_path='data/dataset',cnt=20):
	cd = ColorDescriptor((8, 12, 3))

	# load the query image and describe it
	query = cv2.imread(query_image)
	features = cd.describe(query)

	# perform the search

	searcher = Searcher(index)
	results = searcher.search(features,cnt)

	# display the query
	# cv2.imshow("Query", query)

	# loop over the results
	result_file=[]
	for (score, resultID) in results:
		result_file.append(result_path+'/'+resultID)
	return result_file

		# load the result image and display it
		# result = cv2.imread(args["result_path"] + "/" + resultID)
		# cv2.imshow("Result", result)
		# cv2.waitKey(0)
