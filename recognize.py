import numpy as np
import cv2 as cv
from glob import glob

DB_DIR="../../img/*"
CAMERA = 0
SIFT = cv.SIFT_create()
BF = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
MIN_MATCH_COUNT = 10
FLANN_INDEX_KDTREE = 1

Flann = cv.FlannBasedMatcher(
    dict(algorithm = FLANN_INDEX_KDTREE, trees = 5), 
    dict(checks = 50)
)


def init(db_dir):
    mem = {}
    
    for cat in glob(DB_DIR):
        cat_name = cat.split('/')[-1]
        mem.update({cat_name:{}})
        for img_name in glob("%s/*" % cat):
            img = cv.imread(img_name, 0)
            kp, des = SIFT.detectAndCompute(img, None)
            img_key = img_name.split('/')[-1]
            h,w = img.shape
            mem[cat_name].update({
                img_key:{
                    'keypoints': [kp, des], 
                    'width':  w, 
                    'height': h,
                }
            })
            
    return mem

def take_shot(camera):
    cap = cv.VideoCapture(camera)
    ret, frame = cap.read()
    img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    img_id = 'out'
    cv.imwrite('/tmp/%s.jpeg' % img_id, img)
    return img 

def recognize(img, mem):
    def compare_kp_des_w_obj(obj_a,obj_b):
        kp_a, des_a = obj_a
        kp_b, des_b = obj_b
        
        matches = [ m for m in Flann.knnMatch(des_a,des_b,k=2) ]

        good = []
        for m,n in matches:
            if m.distance < 0.7*n.distance:
                good.append(m)
        
        good = [] if len(good) < MIN_MATCH_COUNT else good
        
        return good
        
    def calc_cat_weight(cat, kp_a, des_a):
        v = 0
        for obj in mem[cat]:
            kp_b, des_b = mem[cat][obj]
            v += compare_kp_des_w_obj((kp_a, des_a),(kp_b, des_b))

        return v
    
    def calc_obj_position(key_points):
        src_pts = np.float32([ kp1[m.queryIdx].pt for m in key_points ]).reshape(-1,1,2)
        dst_pts = np.float32([ kp2[m.trainIdx].pt for m in key_points ]).reshape(-1,1,2)
        M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC,5.0)

        h,w = img1.shape
        pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
        dst = cv.perspectiveTransform(pts,M)
        img2 = cv.polylines(img2,[np.int32(dst)],True,255,3, cv.LINE_AA)        
        
    kp_shot, des_shot = SIFT.detectAndCompute(img, None)
    
    res = {}
    for cat in mem:
        key_points = calc_cat_weight(cat, kp_shot, des_shot)
        position = calc_obj_position(key_points)
        res.update(
            {
                cat:{
                    "weight": len(key_points),
                    "position": position,
                }
            }
        )
        
        
    return(res)
    
      
if __name__ == "__main__":
    db = init(DB_DIR)
    img = take_shot(CAMERA)
    variants = recognize(img, db)
    print(variants)
