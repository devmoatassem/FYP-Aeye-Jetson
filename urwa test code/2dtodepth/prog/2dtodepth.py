#0 means covered
#1 means clear

#from firebase import Firebase
import sys
import os
import datetime
import geocoder
import torch
import pyttsx3
import numpy as np
import cv2
from scipy import misc
from options.train_options import TrainOptions
from loaders import aligned_data_loader
from models import pix2pix_model


def finalcommand(s1, s2, s3, s4):
	s1_black = np.count_nonzero(s1 >= 195)
	s1_total_count = np.count_nonzero(s1 >= 0)
	s2_black = np.count_nonzero(s2 >= 195)
	s2_total_count = np.count_nonzero(s2 >= 0)
	s3_black = np.count_nonzero(s3 >= 195)
	s3_total_count = np.count_nonzero(s3 >= 0)
	s4_black = np.count_nonzero(s4 >= 195)
	s4_total_count = np.count_nonzero(s4 >= 0)
	print(s1_black,s2_black,s3_black,s4_black)
	print(s1_total_count,s2_total_count,s3_total_count,s4_total_count)
	if (s1_black+s2_black)/(s1_total_count+s2_total_count) >= 0.06:
		left = 0
	else:
		left = 1
	if (s2_black+s3_black)/(s2_total_count+s3_total_count) >= 0.06:
		center = 0
	else:
		center = 1
	if (s3_black+s4_black)/(s3_total_count+s4_total_count) >= 0.06:
		right = 0
	else:
		right = 1

	return [left, center, right]


# def time():
# 	now = datetime.datetime.now()
# 	today = datetime.date.today()
# 	current_date = today.strftime("%B %d, %Y")
# 	current_time = now.strftime("%H:%M:%S")
# 	dateinfo = current_date + ' ' + current_time
# 	return dateinfo

def main():
	# config = {
	# 	"apiKey": "AIzaSyBkQ5z8Rs5IRP4lHoiWyXV9XVQHjAh-sEI",
	# 	"authDomain": "a-eye-for-the-blind.firebaseapp.com",
	# 	"storageBucket": "a-eye-for-the-blind.appspot.com",
	# 	"databaseURL": "https://a-eye-for-the-blind-default-rtdb.firebaseio.com/",
	# }
	# uid = "^^^^^^^^^^^"  # unique user ID, must set before running
	# email = 'saranggoel06@gmail.com'
	# password = '##########'
	# firebase = Firebase(config)
	# db = firebase.database()
	# auth = firebase.auth()
	# storage = firebase.storage()

	# user = auth.sign_in_with_email_and_password(email, password)
	# user = auth.refresh(user['refreshToken'])

	# if uid == "" or email == "" or password == "":
	# 	print("Please set user UID, email, or password in the lines above!")
	# 	sys.exit()

	engine = pyttsx3.init()
	BATCH_SIZE = 1
	eval_num_threads = 2
	opt = TrainOptions().parse()  # set CUDA_VISIBLE_DEVICES before import torch
	model = pix2pix_model.Pix2PixModel(opt)
	torch.backends.cudnn.enabled = True
	torch.backends.cudnn.benchmark = True
	best_epoch = 0
	global_step = 0
	model.switch_to_eval()
	video_list = 'infile1/'
	save_path = 'outfile/'
	# uid = 'yQowLXfAMddiITuMFASMoKlSGyh1'
	# initialize the camera
	cam = cv2.VideoCapture(0)  # 0 -> index of camera
	x = 0
	current_datetime = datetime.datetime.now()
	# date_string = current_datetime.date().strftime('%Y-%m-%d')
	# time_string = current_datetime.time().strftime('%H:%M:%S')

	while True:
		s, img = cam.read()
		#cv2.imread('E:/FYP/A-Eye_For_the_Blind-testing/2dtodepth/infile/Walking-slowly-busy-sidewalk.jpg', cv2.IMREAD_COLOR)  # save image
		
		cv2.imwrite('infile1/filename.jpg', img)  # save image
		# filename = f"{date_string} {time_string}"
		# storage.child(f"images/i{str(x)}.jpg").put("D:/A-Eye For The Blind/2dtodepth/infile1/filename.jpg", user['idToken'])
		# url = storage.child(f"images/i{str(x)}.jpg").get_url(user['idToken'])
		# data = {f"i{str(x)}": f"{url}"}
		# db.child(f"users/{uid}").child("images").update(data)
		video_data_loader = aligned_data_loader.DAVISDataLoader(video_list, BATCH_SIZE)
		video_dataset = video_data_loader.load_data()
		for i, data in enumerate(video_dataset):
			stacked_img = data[0]
			targets = data[1]
			output = model.run_and_save_DAVIS(stacked_img, targets, save_path)
			height, width, _ = output.shape
			width_cutoff = width // 2
			half1 = output[:, :width_cutoff]
			half2 = output[:, width_cutoff:]
			width_cutoff = width // 4
			s1 = half1[:, :width_cutoff]
			s2 = half1[:, width_cutoff:]
			s3 = half2[:, :width_cutoff]
			s4 = half2[:, width_cutoff:]
			commands = finalcommand(s1, s2, s3, s4)
			print(commands)
			if commands[1] == 0:
				if commands[0] == 0 and commands[2] == 0:
					engine.say("STOP!")
					print("STOP!")
				elif commands[0] == 1 and commands[2] == 0:
					engine.say("Move right.")
					print("Move right.")
				elif commands[0] == 0 and commands[2] == 1:
					engine.say("Move left.")
					print("Move left.")
				else:
					engine.say("Stop.")
					print("Stop.")
			if commands[1] == 1:
				if commands[0] == 1 and commands[2] == 1:
					engine.say("STOP!")
					print("STOP!")
				elif commands[0] == 0 and commands[2] == 1:
					engine.say("Move right.")
					print("Move right.")
				elif commands[0] == 1 and commands[2] == 0:
					engine.say("Move left.")
					print("Move left.")
				else:
					engine.say("STOP!")
					print("STOP!")
			engine.runAndWait()
		os.remove("infile1/filename.jpg")
		x += 1
		if cv2.waitKey(40) == ord('a'):
			break
	cam.release()


if __name__ == '__main__':
	main()
