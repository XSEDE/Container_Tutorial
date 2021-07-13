#!/usr/bin/env python3
import argparse
import sys
import parallel_mandle as parman
import numpy as np

#    origin=(-1.4011552,0) #easy Feigenbaum(?) point?
#def zoom_loop(start_win_size=2,fin_win_size=0.005,num_steps=2,origin=[-1.4011552,0],output_file="newzoom.gif",numprocs=2):
def zoom_loop(start_win_size,fin_win_size,num_steps,giftime,origin,output_file,numprocs):
#TODOs:
# Add MPI support
# -- 1 frame per cores?
# -- stripe frames across cores?
  gifstep=[]
 
  for i in np.geomspace(start_win_size,fin_win_size,num=num_steps):

    up_left_corn=[origin[0]-(i/2.0),origin[1]-(i/2.0)]
    gifstep.append(parman.mandlebrot_frame(upper_left_corner=up_left_corn,window_size=i,nprocs=numprocs))
  
  gifstep[0].save(output_file,format="GIF",append_images=gifstep[1:],save_all=True,duration=giftime,loop=0)

def main():
    #This will eventually hold the argparsing & maybe file-writing.
#Example file open
#  try:
#    with open(file_name,'x') as script_file: #"w" for write, "a" for append, "x" checks for file exist, "r" for read
#      filename.write(script_head+script_imports+script_main)
#  except Exception as err:
#    print("IOError:",err) 

  parser=argparse.ArgumentParser()
  parser.add_argument("output_file",type=str,help="Output filename - in GIF format",default="newzoom.gif")
  parser.add_argument("-n","--nprocs",type=int,help="Number of multiprocessing threads to spawn",action="store",default=2)
  parser.add_argument("-d","--dur",type=int,help="Duration of GIF in microseconds",action="store",default=100)
  parser.add_argument("-s","--nsteps",type=int,help="Number of steps in the zoom",action="store",default=2)
  parser.add_argument("-w","--swin",type=float,help="Size of the starting frame",action="store",default=2)
  parser.add_argument("-f","--fwin",type=float,help="Size of the ending frame",action="store",default=0.005)
  parser.add_argument("-o","--origin",type=float,help="Center of the frame in c-space, space delimited",nargs=2,action="store",default=[-1.401152,0])
  args=parser.parse_args()
#  if args.flag:
#    print("Flag turned on")
#  print("This is an argument:",args.string_arg)
# Add args for starting boundary, origin, final boundary, steps
  zoom_loop(start_win_size=args.swin,fin_win_size=args.fwin,origin=args.origin,num_steps=args.nsteps,numprocs=args.nprocs,output_file=args.output_file,giftime=args.dur)


if __name__ == '__main__':
  main()
