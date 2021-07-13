#!/usr/bin/env python3
from math import sqrt
import numpy as np
from PIL import Image
from multiprocessing import Pool

def mandle_iterate(c):
#def iterate(x_c,y_c):
# we want the set of all x_c,y_c for which
# mandle stays below 2
# Otherwise, return the # of iterations 
# - max counts as non-divergence?
  x_c = c[0]
  y_c = c[1]
  x,y,count = 0,0,0
  cur_mag=0
  max_iters=256
  while count < max_iters and cur_mag <= 2:
    cur_mag=magnitude(mandle(x_c,y_c,x,y)) 
    x,y = mandle(x_c,y_c,x,y)
#    print(cur_mag,x,count)
    count += 1
  return count;

def magnitude(z):
  return sqrt(z[0]**2 + z[1]**2)

def mandle(x_c,y_c,x,y):
# f_c(z) = z^2 + c
# iterate around 0 - so x_c and y_c are fixed
# x real; y imaginary
#(a+bi)**2 = (a**2 - b**2 + 2abi)
   return (x**2 - y**2 + x_c,2*x*y + y_c)

def mandlebrot_frame(pixels=512,upper_left_corner=(-1.5,-1.5),window_size=2,nprocs=4):

  def to_coords(c):
  # show a square of length window_size from (upper_left_corner,upper_left_corner) (to upper_left_corner+window_size)
  # this f'n takes a tuple of int x,y coords, returns a float tuple of 'real' coords
  # or it would if we didn't live in a magic fairy land of dynamically typed variables.
    return ((window_size / pixels * c[0]) + upper_left_corner[0],(window_size / pixels * c[1]) + upper_left_corner[1])
 
#Neat babybrot at: 
#parallel_mandle.mandlebrot_main(upper_left_corner=(0.439,0.369),window_size=0.01,pixels=4096)


  
#  coords_list = list(map(to_coords(c), [(x,y) 
  coords_list = map(to_coords, [(x,y) 
                            for x in range(0,pixels) 
                             for y in range (0,pixels)])

#  print("Coords_list_len =", len(coords_list))
#  print("Coords_list =", coords_list)
  with Pool(processes=nprocs) as pool:
    pic_list=pool.map(mandle_iterate,coords_list)
#  print("pic_len =",len(pic_list))
  pic = np.reshape(np.array(pic_list),(pixels,pixels))
#  print("pic_shape =",np.shape(pic))
#  print("Pic:",pic)
#  try:
#    with open("mandle_raw.txt",'wb') as mandle_file:
#      np.savetxt(mandle_file,pic,fmt="%4.8f",delimiter=' ')
#  except Exception as err:
#    print("IOError:",err) 
  out_pic=Image.fromarray(pic.astype(np.uint8),'L')
  return out_pic

def mandlebrot_main():
  default_pic=mandlebrot_pic()
  filename="par_outfile.png"
  default_pic.save(filename,"PNG")

if __name__ == '__main__':
  mandlebrot_main()
