#!/usr/bin/env python
#coding=utf-8


from PIL import Image

def vfx(img, threshold, bg_level , color=False):
 
    threshold = min(100,max(0,threshold))
    width, height = img.size
    dst_img = Image.new("RGBA", (width, height))
    if img.mode != "RGBA":
        img = img.convert("RGBA")
    pix = img.load()
    dst_pix = dst_img.load()

   
    for w in xrange(width):
        for h in xrange(height):
            if w == 0 or w == width - 1 \
               or h == 0 or h == height - 1:
                continue
            
            
            around_wh_pixels = [pix[i, j][:3] for j in xrange(h-1, h+2) for i in xrange(w-1, w+2)]
            exclude_wh_pixels = tuple(around_wh_pixels[:4] + around_wh_pixels[5:])
            RGB = map(lambda l: int(sum(l) / len(l)), zip(*exclude_wh_pixels))
            cr_p = pix[i, j] 
            cr_draw = all([abs(cr_p[i] - RGB[i]) >= threshold for i in range(3)])
            if cr_draw:
                dst_pix[w, h] = 0, 0, 0, cr_p[3]
            else:
                avg  = (pix[w,h][0]+pix[w,h][1]+pix[w,h][2])/3
                pixals = min(255,bg_level + avg)
                if color:
                    red = pix[w,h][0] - avg
                    green = pix[w,h][1] - avg
                    blue = pix[w,h][2] - avg
                    pixals = (avg + int(red*color), avg + int(green*color),avg + int(blue*color))
                    dst_pix[w, h] = pixals
                else:
                    dst_pix[w, h] = (pixals,pixals,pixals)

    return dst_img

if __name__ == "__main__":
    
    import sys, os, time

   
   
    path = sys.argv[1]
    start = time.time()
    imgg = Image.open(path)
    count = 0
    bg_level = 255
    if not os.path.exists("out"):
        os.makedirs('out')
    for threshold in range(60,10,-1):
        print count ,'drawing pencil'
        img = vfx(imgg, threshold , bg_level)
        img.save('out/' +str(count).zfill(4)+'.png', 'PNG')
        count = count +1

    for bg_level in range(250,0-5,-5):
        print count, 'apply black and white'
        img = vfx(imgg, threshold , bg_level)
        img.save('out/' +str(count).zfill(4)+'.png', 'PNG')
        count = count +1
    for threshold in range(10,100+10,10):
        print count ,'removing  pencil'
        img = vfx(imgg, threshold , bg_level)
        img.save('out/' +str(count).zfill(4)+'.png', 'PNG')
        count = count +1
    count = count -1
    for color in range(1,100+2,2):
        print count ,'coloring'
        color = color/100.0
        img = vfx(imgg, threshold , bg_level, color)
        img.save('out/' +str(count).zfill(4)+'.png', 'PNG')
        count = count +1
    print count , 'images created!'
    cmd = 'ffmpeg -framerate 10 -i out/%04d.png -c:v libx264 -r 30 -pix_fmt yuv420p pencil-bw-color.mp4'
    os.system(cmd)


        


    end = time.time()
    print 'It all spends %f seconds time' % (end-start)
