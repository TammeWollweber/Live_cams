import pickle

file_name = "colormap1.pkl"
#sample_list = [(0, 0, 0),(4, 5, 61),(84, 42, 55),(15, 87, 60),(208, 17, 141),(255, 255, 255)]
#sample_list = [(0, 255, 255, 255), (255, 255, 0, 255), (0, 0, 0, 255), (0, 0, 255, 255), (255, 0, 0, 255)]
#sample_list = [(0., 1, 1,), (.2, 0, 0), (.48, 0, 0), (.728, 1, 1), (1, .5, .5)]
#sample_list = [(0.,0.,125,255),(0.,125,255,255),(125,255,125,255),(255,125,0.,255),(125,0.,0.,255)]
sample_list = [(0.,0.,255),(255,0.,0.),(0.,255,0.),(0.,255,255),(255,255,0.)]


open_file = open(file_name, "wb")
pickle.dump(sample_list, open_file)
open_file.close()
favorite_color = pickle.load(open("colormap1.pkl", "rb"))
loaded_list = favorite_color
print("loaded_list: ",loaded_list)