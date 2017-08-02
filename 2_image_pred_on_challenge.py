import numpy as np
import tensorflow as tf
import os
import cv2
import random
import linecache

lenth=96
n_inputs=lenth*lenth*32//64
n_hidden_units = 2048
n_outputs=n_inputs

img_num=[362, 358, 211, 321, 239, 302, 311, 310, 240, 340, 248, 268, 240, 389, 348, 293, 287, 298, 314, 336,
         261, 273, 351, 302, 272, 284, 252, 303, 292, 247, 282, 312, 308, 282, 245, 356, 316, 324, 327, 336,
         414, 267, 285, 311, 325, 271, 288, 347, 356, 353, 318, 336, 320, 354, 350, 339, 304, 409, 267, 405,
         354, 336, 314, 282, 287, 320, 374, 274, 307, 167, 276, 212, 294, 289, 285, 325, 297, 282, 331, 258,
         296, 307, 319, 397, 256, 263, 295, 349, 311, 255, 312, 332, 264, 286, 323, 320, 293, 275, 354, 346,
         393, 369, 280, 226, 277, 287, 310, 329, 318, 325, 293, 302, 320, 327, 305, 239, 282, 302, 321, 355,
         319, 369, 321, 234, 274, 252, 205, 258, 288, 289, 267, 318, 294, 376, 347, 393, 379, 330, 359, 334,
         368, 365, 321, 291, 311, 299, 361, 304, 361, 249, 355, 359, 410, 319, 369, 348, 279, 283, 373, 405,
         406, 363, 320, 357, 368, 415, 415, 262, 352, 430, 423, 374, 401, 411, 417, 399, 254, 380, 313, 335,
         407, 256, 284, 316, 273, 291, 260, 314, 318, 293, 317, 277, 272, 227, 229, 237, 263, 296, 387, 313,
         312, 224, 285, 293, 394, 359, 248, 324, 308, 250, 293, 375, 315, 367, 328, 261, 222, 332, 358, 396,
         316, 336, 301, 214, 281, 285, 267, 275, 222, 364, 179, 348, 283, 316, 306, 274, 210, 310, 353, 349,
         314, 380, 354, 370, 313, 302, 425, 316, 316, 397, 381, 311, 290, 273, 332, 376, 296, 387, 356, 367,
         267, 330, 306, 375, 351, 308, 408, 392, 293, 301, 328, 306, 326, 311, 307, 313, 263, 420, 397, 248,
         324, 361, 363, 370, 311, 421, 353, 365, 361, 432, 300, 393, 350, 301, 419, 282, 296, 307, 341, 271,
         333, 310, 292, 318, 310, 280, 219, 301, 369, 362, 430, 398, 331, 377, 302, 290, 319, 304, 308, 374,
         414, 292, 332, 433, 276, 265, 429, 381, 380, 328, 297, 329, 421, 258, 434, 398, 312, 307, 288, 286,
         349, 300, 391, 279, 299, 350, 433, 368, 420, 376, 398, 425, 313, 301, 292, 333, 368, 301, 384, 324,
         301, 378, 339, 483, 401, 354, 313, 373, 302, 313, 331, 332, 314, 260, 327, 323, 320, 375, 306, 270,
         297, 351, 331, 261, 270, 270, 349, 398, 330, 331, 269, 356, 284, 291, 359, 412, 290, 391, 318, 334,
         371, 338, 364, 339, 321, 384, 333, 310, 385, 321, 354, 328, 354, 344, 276, 279, 391, 361, 345, 395,
         308, 366, 364, 310, 264, 364, 256, 358, 306, 397, 335, 403, 375, 280, 390, 243, 370, 417, 366, 400,
         321, 358, 321, 367, 317, 339, 260, 287, 398, 346, 419, 362, 317, 412, 261, 305, 295, 330, 469, 415,
         310, 436, 208, 417, 248, 239, 338, 334, 315, 231, 262, 327, 290, 269, 227, 448, 433, 322, 419, 220,
         419, 435, 418, 291, 247, 238, 303, 425, 286, 404, 442, 229, 425, 302, 244, 278, 410, 437, 292, 381,
         427, 268, 227, 286, 307, 231, 467, 239, 421, 279, 423, 316, 309, 296, 289, 430, 451, 346, 423, 301,
         442, 426, 418, 450, 444, 425, 280, 420, 367, 413, 453, 411, 286, 264, 279, 351, 418, 325, 308, 419,
         272, 261, 402, 316, 235, 420, 341, 228, 424, 406, 319, 207, 406, 430, 254, 404, 203, 388, 215, 409,
         413, 452, 315, 371, 357, 300, 420, 378, 240, 402, 341, 376, 280, 216, 388, 396, 277, 286, 333, 300,
         312, 445, 266, 255, 319, 250, 366, 239, 431, 403, 411, 178, 292, 220, 280, 235, 264, 396, 309, 461,
         288, 416, 195, 430, 422, 267, 249, 295, 385, 300, 275, 280, 361, 423, 407, 433, 344, 293, 310, 432,
         290, 312, 393, 418, 283, 264, 276, 273, 415, 442, 446, 441, 435, 410, 444, 454, 441, 255, 254, 411,
         454, 350, 299, 253, 222, 242, 329, 420, 424, 413, 405, 263, 277, 410, 419, 285, 289, 456, 472, 306,
         447, 288, 372, 388, 357, 309, 456, 317, 437, 306, 309, 202, 414, 444, 488, 232, 292, 201, 467, 441,
         256, 439, 397, 310, 292, 185, 298, 428, 376, 419, 417, 252, 233, 300, 313, 335, 441, 353, 372, 337,
         429, 334, 294, 276, 403, 191, 379, 300, 325, 449, 298, 462, 269, 442, 398, 459, 226, 351, 288, 216,
         283, 261, 412, 313, 440, 416, 236, 387, 454, 415, 258, 355, 332, 475, 457, 433, 399, 274, 304, 233,
         426, 296, 258, 395, 190, 353, 313, 446, 425, 285, 280, 454, 437, 437, 320, 393, 208, 432, 288, 330,
         399, 259, 303, 473, 216, 230, 397, 419, 303, 432, 418, 437, 325, 277, 270, 223, 336, 219, 388, 277,
         447, 315, 301, 316, 469, 200, 297, 420, 347, 438, 284, 431, 260, 423, 228, 413, 479, 348, 306, 436,
         474, 238, 350, 328, 488, 315, 480, 441, 345, 459, 427, 433, 437, 449, 211, 375, 323, 463, 450, 462, 389, 445, 328, 455, 312, 468, 316, 321, 317, 330, 441, 317, 240, 425, 430, 453, 444, 301, 446, 300, 441, 435, 352, 446, 458, 427, 306, 375, 401, 296, 418, 460, 288, 301, 293, 276, 402, 423, 460, 400, 424, 487, 406, 456, 380, 416, 443, 433, 465, 419, 342, 290, 395, 328, 393, 257, 294, 243, 425, 464, 430, 282, 322, 388, 311, 229, 320, 320, 452, 419, 420, 456, 332, 403, 437, 291, 298, 315, 292, 426, 204, 456, 458, 448, 312, 284, 339, 284, 396, 290, 280, 313, 397, 212, 451, 377, 298, 407, 448, 401, 442, 448, 320, 303, 313, 326, 464, 431, 306, 340, 301, 433, 246, 343, 355, 323, 393, 473, 482, 349, 417, 303, 329, 296, 478, 309, 277, 407, 407, 459, 309, 418, 415, 353, 373, 310, 414, 300, 397, 457, 272, 375, 404, 411, 325, 323, 424, 335, 392, 408, 230, 389, 291, 178, 291, 434, 265, 302, 414, 407, 454, 381, 432, 429, 450, 294, 433, 354, 303, 360, 455, 492, 261, 337, 444, 438, 412, 180, 233, 273, 256, 452, 493, 442, 423, 380, 442, 207, 279, 492, 396, 300, 405, 409, 361, 370, 306, 413, 325, 315, 419, 293, 306, 460, 304, 199, 337, 249, 213, 192, 180, 368, 231, 203, 290, 482, 398, 290, 404, 376, 450, 294, 320, 478, 445, 293, 216, 427, 277, 448, 438, 448, 290, 481, 485, 322, 309, 303, 353, 411, 263, 413, 324, 375, 297, 212, 328, 450, 399, 239, 391, 275, 322, 262, 317, 492, 437, 471, 428, 314, 287, 310, 304, 382, 359, 255, 428, 286, 223, 433, 425, 238, 310, 405, 246, 306, 443, 428, 296, 313, 261, 431, 437, 428, 395, 458, 300, 367, 354, 445, 181, 398, 439, 181, 428, 319, 287, 316, 274, 432, 394, 339, 450, 435, 304, 294, 431, 273, 424, 355, 300, 335, 285, 431, 306, 438, 328, 422, 402, 313, 460, 435, 287, 257, 445, 466, 322, 253, 433, 419, 253, 435, 413, 364, 431, 433, 437, 204, 258, 432, 260, 267, 438, 278, 464, 428, 235, 416, 202, 280, 215, 411, 180, 276, 370, 434, 421, 432, 179, 454, 388, 268, 378, 432, 274, 408, 279, 191, 262, 396, 298, 213, 284, 345, 282, 413, 356, 203, 214, 276, 390, 449, 266, 447, 261, 426, 366, 295, 348, 450, 317, 346, 299, 273, 400, 267, 415, 276, 458, 307, 424, 415, 216, 273, 467, 407, 424, 272, 479, 423, 410, 330, 386, 324, 423, 276, 338, 217, 461, 411, 482, 282, 251, 343, 240, 345, 307, 417, 222, 431, 465, 265, 333, 250, 414, 265, 406, 419, 439, 454, 304, 219, 405, 295, 265, 242, 384, 428, 198, 163, 423, 218, 458, 192, 291, 271, 214, 438, 174, 358, 370, 439, 414, 255, 308, 388, 387, 414, 172, 408, 401, 274, 414, 390, 189, 399, 282, 354, 259, 395, 363, 399, 390, 275, 383, 395, 272, 394, 415, 324, 454, 417, 399, 293, 379, 261, 410, 389, 376, 270, 401, 407, 316, 207, 356, 384, 372, 465, 249, 429, 296, 295, 382, 439, 260, 290, 373, 400, 449, 379, 194, 442, 377, 276, 239, 277, 445, 283, 422, 451, 289, 260, 425, 407, 295, 424, 390, 419, 444, 266, 324, 295, 447, 405, 321, 307, 459, 454, 295, 405, 370, 442, 419, 261, 396, 427, 307, 437, 270, 393, 423, 242, 431, 305, 405, 400, 259, 413, 443, 397, 453, 424, 263, 327, 426, 293, 315, 270, 458, 355, 418, 439, 426, 434, 260, 267, 303, 306, 291, 451, 443, 442, 418, 243, 287, 281, 406, 467, 416, 338, 362, 465, 226, 349, 211, 443, 295, 407, 453, 286, 321, 408, 412, 415, 466, 421, 406, 252, 289, 244, 456, 271, 388, 432, 274, 449, 436, 412, 416, 431, 473, 441, 452, 399, 435, 379, 423, 427, 309, 404, 417, 383, 289, 443, 470, 405, 416, 432, 435, 212, 314, 398, 194, 298, 185, 200, 426, 287, 193, 461, 217, 371, 216, 276, 416, 283, 256, 341, 187, 285, 424, 223, 285, 166, 300, 309, 291, 251, 458, 276, 336, 438, 302, 309, 309, 201, 379, 454, 312, 459, 275, 389, 242, 280, 162, 414, 333, 368, 379, 236, 452, 311, 192, 300, 205, 325, 182, 314, 325, 294, 200, 225, 232, 426, 274, 297, 415, 384, 287, 457, 387, 364, 204, 302, 351, 317, 304, 247, 208, 247, 207, 316, 428, 424, 197, 441, 296, 419, 401, 169, 302, 179, 322, 423, 263, 456, 418, 249, 244, 260, 467, 426, 421, 403, 299, 209, 256, 291, 254, 274, 296, 244, 320, 434, 276, 358, 463, 390, 418, 284, 301, 289, 219, 302, 277, 440, 375, 354, 387, 295, 396, 281, 283, 292, 313, 330, 221, 431, 364, 453, 287, 197, 289, 203, 202, 400, 205, 194, 210, 191, 185, 344, 303, 229, 212, 275, 218, 371, 215, 287, 410, 190, 342, 283, 304, 257, 268, 386, 259, 205, 215, 292, 312, 271, 328, 304, 345, 458, 225, 204, 248, 209, 203, 211, 233, 330, 342, 189, 308, 206, 236, 222, 295, 285, 241, 306, 485, 280, 299, 335, 380, 413, 324, 318, 329, 366, 294, 211, 210, 319, 275, 311, 298, 327, 352, 334, 227, 464, 276, 229, 331, 453, 261, 255, 328, 271, 381, 421, 208, 290, 345, 257, 331, 310, 244, 217, 328, 196, 263, 309, 239, 428, 204, 280, 413, 205, 299, 228, 172, 295, 194, 418, 276, 181, 197, 442, 200, 352, 314, 426, 333, 250, 450, 314, 246, 297, 378, 454, 206, 398, 438, 364, 423, 251, 333, 277, 299, 302, 200, 436, 394, 442, 377, 302, 303, 364, 440, 259, 322, 470, 448, 315, 174, 199, 329, 275, 354, 196, 308, 307, 352, 302, 299, 327, 311, 329, 262, 388, 293, 493, 187, 338, 224, 440, 325, 237, 269, 410, 226, 266, 434, 314, 286, 181, 189, 236, 406, 370, 301, 288, 336, 391, 329, 206, 197, 335, 355, 335, 207, 208, 334, 354, 352, 233, 451, 299, 419, 298, 326, 416, 422, 480, 318, 445, 407, 298, 235, 470, 464, 289, 316, 191, 218, 309, 181, 297, 292, 352, 282, 441, 443, 258, 465, 220, 439, 285, 292, 329, 307, 234, 214, 200, 419, 414, 229, 341, 379, 365, 291, 230, 234, 241, 285, 195, 214, 335, 299, 240, 241, 259, 289, 310, 431, 261, 322, 203, 314, 218, 254, 288, 277, 230, 332, 245, 265, 276, 190, 222, 416, 423, 423, 362, 299, 319, 182, 440, 184, 227, 200, 405, 340, 235, 300, 300, 266, 264, 280, 434, 270, 274, 292, 425, 446, 262, 434, 302, 289, 355, 331, 462, 435, 268, 280, 253, 192, 272, 312, 324, 267, 226, 297, 293, 290, 176, 329, 260, 193, 351, 375, 310, 219, 295, 448, 290, 473, 277, 284, 246, 199, 276, 407, 187, 172, 169, 304, 303, 427, 405, 425, 314, 424, 241, 297, 320, 312, 398, 188, 292, 299, 464, 172, 151, 202, 312, 305, 221, 218, 197, 341, 439, 426, 354, 200, 169, 259, 192, 286, 240, 289, 181, 404, 342, 169, 441, 296, 213, 249, 409, 203, 297, 339, 225, 238, 439, 413, 326, 326, 191, 441, 267, 218, 246, 248, 442, 233, 304, 250, 191, 225, 433, 397, 217, 386, 296, 345, 199, 301, 427, 227, 247, 218, 224, 347, 212, 229, 440, 406, 345, 447, 213, 402, 206, 249, 376, 301, 390, 289, 236, 181, 211, 176, 429, 284, 424, 274, 472, 446, 177, 333, 250, 186, 195, 295, 462, 431, 455, 346, 174, 266, 424, 189, 382, 376, 257, 188, 210, 347, 252, 198, 218, 379, 199, 315, 203, 342, 181, 246, 330, 358, 254, 222, 269, 411, 218, 313, 315, 302, 347, 273, 274, 487, 456, 204, 324, 277, 375, 280, 342, 445, 354, 239, 331, 198, 299, 200, 359, 431, 456, 294, 370, 429, 205, 294, 245, 447, 318, 309, 444, 315, 171, 320, 347, 299, 323, 285, 303, 285, 301, 225, 462, 215, 218, 352, 246, 430, 305, 321, 171, 467, 484, 337, 299, 280, 269, 268, 308, 175, 295, 424, 326, 204, 241, 312, 198, 217, 236, 332, 253, 438, 362, 229, 297, 465, 202, 248, 317, 319, 253, 217, 302, 292, 332, 178, 252, 359, 329, 357, 305, 300, 342, 279, 197, 301, 428, 295, 423, 462, 428, 170, 283, 218, 231, 311, 459, 356, 443, 198, 345, 175, 257, 306, 311, 232, 335, 439, 257, 283, 323, 289, 307, 228, 375, 440, 265, 217, 266, 275, 258, 182, 466, 318, 285, 393, 224, 291, 298, 202, 229, 253, 227, 226, 213, 256, 214, 239, 257, 209, 304, 454, 258, 307, 346, 220, 268, 396, 307, 289, 246, 266, 476, 215, 370, 237, 229, 221, 233, 307, 457, 214, 248, 243, 442, 222, 341, 287, 420, 444, 317, 225, 231, 319, 472, 466, 340, 259, 270, 205, 494, 258, 449, 340, 306, 435, 276, 325, 263, 349, 300, 354, 317, 455, 494, 391, 274, 256, 207, 336, 254, 323, 297, 227, 233, 480, 235, 294, 389, 341, 395, 251, 426, 278,
         304, 464, 444, 327, 365, 307, 209, 252, 244, 310, 214, 308, 396, 267, 303, 326, 207, 305, 349]#, 209, 188]
#print(len(img_num))

# image_input= img_num - [4 * x / x for x in range(1, 51)]
def gray2binary(a):
    for i in range(len(a)):
        if a[i]>60:
            a[i]=1
        elif a[i]<=60:
            a[i]=0
    return a

def random_index(rate):

    # 参数rate为list<int>

    start = 0
    randnum = random.randint(1, sum(rate))
    index_= 0
    for index_, item in enumerate(rate):
        start += item
        if randnum <= start:
            break
    return index_

def get_train_batch():
    rate = img_num
    ran_sent = random_index(rate)
    #print('ran_sent',ran_sent)
    #f = open('./list/Bruce_list_folder_%d.txt' % ran_sent, 'r')

    ran = np.random.randint(0,(rate[ran_sent]-3),size=10,dtype='int')
    #print('ran',ran)
    image = []
    label = []
    n_pic = ran #np.random.randint(600,5996)
    # print(n_pic)
    for i in range(10):
        image_0=[]
        for j in range(2):
            dir = linecache.getline('./list/Bruce_list_folder_%d.txt' % ran_sent, (n_pic[i] + j +1))
            dir = dir.strip('\n')
            # print(dir)
            # dir = f.readlines()[5]#[(n_pic[i]+j)]
            frame_0 = cv2.imread(dir, 0)
            # frame_0 = add_noise(frame_0, n = noise)
            frame_0 = cv2.resize(frame_0, (lenth, lenth))
            frame_0 = np.array(frame_0).reshape(-1)
            frame_0 = frame_0 / 255.0
            image_0.append(frame_0)
        image.append(image_0)
    # print(np.shape(image))
    # np.transpose(image,[1,0,2])
    # print(np.shape(image))
    for i in range(10):
        dir = linecache.getline('./list/Bruce_list_folder_%d.txt' % ran_sent, (n_pic[i] + 3))
        dir = dir.strip('\n')
        #dir = f.readlines()[n_pic[i] + 2].strip('\n')
        frame_1 = cv2.imread(dir, 0)
        frame_1 = cv2.resize(frame_1, (lenth,lenth))
        frame_1 = np.array(frame_1).reshape(-1)
        frame_1 = gray2binary(frame_1)
        label.append(frame_1)
    return np.array(image,dtype='float') , np.array(label,dtype='float')

def get_test_batch(): # n_pic[600,5996]
    ran = np.random.randint(0, 185, size=10, dtype='int')
    image = []
    label = []
    n_pic =  ran#range(n,n+10)  # np.random.randint(600,5996)
    #print(n_pic)
    #f = open('./list/Bruce_list_folder_2340.txt', 'r')
    for i in range(10):
        image_0 = []
        for j in range(2):
            dir = linecache.getline('./list/Bruce_list_folder_2341.txt', (n_pic[i] + j + 1))
            dir = dir.strip('\n')
            #print(dir)
            frame_0 = cv2.imread(dir, 0)
            # frame_0 = add_noise(frame_0, n = noise)
            frame_0 = cv2.resize(frame_0, (lenth, lenth))
            frame_0 = np.array(frame_0).reshape(-1)
            frame_0 = frame_0 / 255.0
            image_0.append(frame_0)
        image.append(image_0)
    for i in range(10):
        dir = linecache.getline('./list/Bruce_list_folder_2341.txt', (n_pic[i] + 3))
        dir = dir.strip('\n')
        frame_1 = cv2.imread(dir, 0)
        frame_1 = cv2.resize(frame_1, (lenth, lenth))
        frame_1 = np.array(frame_1).reshape(-1)
        frame_1 = gray2binary(frame_1)
        label.append(frame_1)
    return np.array(image, dtype='float'), np.array(label, dtype='float'),n_pic

# def get_show_batch(): # n_pic[600,5996]
#     ran = np.random.randint(5800,6000, size=10, dtype='int')
#     image = []
#     label = []
#     #label_0 = []
#     n_pic = ran  # np.random.randint(600,5996)
#     for i in range(10):
#         image_0 = []
#         for j in range(4):
#             frame_0 = cv2.imread('./cropedoriginalUS2/%d.jpg' % (n_pic[i]+ j), 0)
#             # frame_0 = add_noise(frame_0, n = noise)
#             frame_0 = cv2.resize(frame_0, (lenth, lenth))
#             frame_0 = np.array(frame_0).reshape(-1)
#             frame_0 = frame_0 / 255.0
#             image_0.append(frame_0)
#         image.append(image_0)
#     for i in range(10):
#         frame_1 = cv2.imread('./cropedoriginalPixel2/%d.jpg' % (n_pic[i] + 4), 0)
#         frame_1 = cv2.resize(frame_1, (lenth, lenth))
#         frame_1 = np.array(frame_1).reshape(-1)
#         frame_1 = gray2binary(frame_1)
#         label.append(frame_1)
#     return np.array(image, dtype='float'), np.array(label, dtype='float')

def input_norm(xs):
    fc_mean, fc_var = tf.nn.moments(
        xs,
        axes=[0],
    )
    scale = tf.Variable(tf.ones([1]))
    shift = tf.Variable(tf.zeros([1]))
    epsilon = 0.001
    # apply moving average for mean and var when train on batch
    ema = tf.train.ExponentialMovingAverage(decay=0.5)

    def mean_var_with_update():
        ema_apply_op = ema.apply([fc_mean, fc_var])
        with tf.control_dependencies([ema_apply_op]):
            return tf.identity(fc_mean), tf.identity(fc_var)

    mean, var = mean_var_with_update()
    xs = tf.nn.batch_normalization(xs, mean, var, shift, scale, epsilon)
    return xs

def batch_norm(Wx_plus_b,out_size):
    fc_mean, fc_var = tf.nn.moments(
        Wx_plus_b,
        axes=[0],  # the dimension you wanna normalize, here [0] for batch
        # for image, you wanna do [0, 1, 2] for [batch, height, width] but not channel
    )
    scale = tf.Variable(tf.ones([out_size]))
    shift = tf.Variable(tf.zeros([out_size]))
    epsilon = 0.001
    # apply moving average for mean and var when train on batch
    ema = tf.train.ExponentialMovingAverage(decay=0.5)
    def mean_var_with_update():
        ema_apply_op = ema.apply([fc_mean, fc_var])
        with tf.control_dependencies([ema_apply_op]):
            return tf.identity(fc_mean), tf.identity(fc_var)
    mean, var = mean_var_with_update()
    Wx_plus_b = tf.nn.batch_normalization(Wx_plus_b, mean, var, shift, scale, epsilon)
    return Wx_plus_b

inputs_ = tf.placeholder(tf.float32, [None, lenth,lenth, 2])
targets_ = tf.placeholder(tf.float32, [None, lenth,lenth, 1])

conv1 = tf.layers.conv2d(inputs_, 32, (5,5), padding='same', activation=tf.nn.relu)
conv1 = tf.layers.max_pooling2d(conv1, (2,2), (2,2), padding='same')
conv1 = batch_norm(conv1,32)
conv2 = tf.layers.conv2d(conv1, 64, (3,3), padding='same', activation=tf.nn.relu)
conv2 = tf.layers.max_pooling2d(conv2, (2,2), (2,2), padding='same')
conv2 = batch_norm(conv2,64)
conv3 = tf.layers.conv2d(conv2, 64, (3,3), padding='same', activation=tf.nn.relu)
conv3 = tf.layers.max_pooling2d(conv3, (2,2), (2,2), padding='same')
conv3 = batch_norm(conv3,64)
conv4 = tf.layers.conv2d(conv3, 128, (3,3), padding='same', activation=tf.nn.relu)
conv4 = tf.layers.max_pooling2d(conv4, (2,2), (2,2), padding='same')
conv4 = batch_norm(conv4,128)
conv5 = tf.layers.conv2d(conv4, 128, (3,3), padding='same', activation=tf.nn.relu)
conv5 = tf.layers.max_pooling2d(conv5, (2,2), (2,2), padding='same')
conv5 = batch_norm(conv5,128)

conv6 = tf.image.resize_nearest_neighbor(conv5, (6,6))
conv6 = tf.layers.conv2d(conv6, 128, (3,3), padding='same', activation=tf.nn.relu)
conv6 = batch_norm(conv6,128)
conv7 = tf.image.resize_nearest_neighbor(conv6, (12,12))
conv7 = tf.layers.conv2d(conv7, 64, (3,3), padding='same', activation=tf.nn.relu)
conv7 = batch_norm(conv7,64)
conv8 = tf.image.resize_nearest_neighbor(conv7, (24,24))
conv8 = tf.layers.conv2d(conv8, 64, (3,3), padding='same', activation=tf.nn.relu)
conv8 = batch_norm(conv8,64)
conv9 = tf.image.resize_nearest_neighbor(conv8, (48,48))
conv9 = tf.layers.conv2d(conv9, 32, (3,3), padding='same', activation=tf.nn.relu)
conv9 = batch_norm(conv9,32)
conv10 = tf.image.resize_nearest_neighbor(conv9, (96,96))
conv10 = tf.layers.conv2d(conv10, 2, (5,5), padding='same', activation=None)# tf.nn.relu)
#conv10 = batch_norm(conv10,2)
#logits_ = tf.layers.conv2d(conv6, 2, (3,3), padding='same', activation=None)
outputs_ = tf.nn.softmax(conv10, dim= -1,name='outputs_')
outputs_ = outputs_[:,:,:,-1]
outputs_ = tf.reshape(outputs_ , [-1,lenth,lenth,1])

cost = tf.reduce_mean(tf.square(tf.reshape(targets_,[-1]) - tf.reshape(outputs_,[-1])))
# loss = tf.nn.softmax_cross_entropy_with_logits(labels=targets_, logits=outputs_)
# cost = tf.reduce_mean(loss)
optimizer = tf.train.AdamOptimizer(0.0005).minimize(cost)
all_saver = tf.train.Saver()
saver = tf.train.import_meta_graph('./Stack_prediction_test_on_Challenge_data/full_train_save/matadata.chkp.meta')

with tf.Session() as sess:
    init = tf.global_variables_initializer()
    sess.run(init)
    saver.restore(sess,tf.train.latest_checkpoint('./Stack_prediction_test_on_Challenge_data/full_train_save/')) # tf.train.latest_checkpoint('./stack_img_pred_saver/')) # './stack_img_pred_saver/data_0.chkp.data-00000-of-00001')
    # loss_history=[]
    # for i in range(20000): #10000
    #     batch, img = get_train_batch()
    #     #print(np.shape(batch))
    #     batch = np.transpose(batch,[0,2,1])
    #     batch= np.reshape(batch,[-1, lenth,lenth, 2])
    #     img= np.reshape(img,[-1,lenth,lenth, 1])
    #     sess.run(optimizer, feed_dict={inputs_: batch, targets_: img})
    #     if i % 200 == 0:
    #         batch_cost = sess.run(cost, feed_dict={inputs_: batch, targets_: img})
    #         # loss_history.append(batch_cost)
    #         print("Batch: {} ".format(i), "Training loss: {:.5f}".format(batch_cost))
    #         all_saver.save(sess, './Stack_prediction_test_on_Challenge_data/full_train_save/matadata.chkp')
    # print("Optimization Finishes!")

    for i in range(0,1000):
        batch_xs, batch_ys, n_pic = get_test_batch()
        batch_xs = np.transpose(batch_xs, [0, 2, 1])
        batch_xs = np.reshape(batch_xs, [-1, lenth, lenth, 2])
        batch_ys = np.reshape(batch_ys, [-1, lenth, lenth, 1])
        image_p = sess.run(outputs_, feed_dict={inputs_: batch_xs, targets_: batch_ys})
        image_p = image_p * 255
        for n in range(10):
            img = np.array(np.reshape(image_p[n], (lenth,lenth)),dtype='int32')
            cv2.imwrite("./Stack_prediction_test_on_Challenge_data/pred_result_challenge_full_1/%d.jpg" % (n_pic[n]+3), img) #, [int(cv2.IMWRITE_JPEG_QUALITY), 100])
        if i%100==0:
            print('%d finished' % i)

    # batch_xs, batch_ys = get_show_batch()
    # batch_xs = np.transpose(batch_xs, [0, 2, 1])
    # batch_xs = np.reshape(batch_xs, [-1, lenth, lenth, 4])
    # batch_ys = np.reshape(batch_ys, [-1, lenth, lenth, 1])
    # # batch_us = np.reshape(batch_us, [-1, lenth, lenth, 1])
    # image_p = sess.run(outputs_, feed_dict={inputs_: batch_xs, targets_: batch_ys})
    # plt.figure(1)
    # f, a = plt.subplots(2, 10, figsize=(10, 2))
    # for i in range(10):
    #     # a[0][i].imshow(np.reshape(ys_0[i], (LONGITUDE, LONGITUDE)))
    #     a[0][i].imshow(np.reshape(batch_ys[i], (lenth, lenth)))
    #     # a[1][i].imshow(np.reshape(batch_xs[i], (24, 24)))
    #     a[1][i].imshow(np.reshape(image_p[i], (lenth, lenth)))
    #     # a[1][0].save("./image_predict_00/%d.jpg" % 0)
    # plt.show()
    print('All finished!')
