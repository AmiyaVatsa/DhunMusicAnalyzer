#import libraries
import numpy as np
import librosa
import librosa.display
import os
import matplotlib.pyplot as plt
import IPython.display as ipd

def audio_comparator(file_1 : str, file_2 : str):
    #loading files
    audio_1, sr = librosa.load(file_1)
    audio_2, _ = librosa.load(file_2, offset = 0.0, duration = 10.0)

    #finding mfccs
    mfccs_1 = librosa.feature.mfcc(y = audio_1, sr = sr, n_mfcc = 13)
    mfccs_2 = librosa.feature.mfcc(y = audio_2, sr = sr, n_mfcc = 13)


    #finding euclidean distance
    dist = np.zeros(shape = (mfccs_1.shape[1], mfccs_2.shape[1]))
    for i in range(mfccs_1.shape[1]):
        for j in range(mfccs_2.shape[1]):
            euclidean = np.linalg.norm(mfccs_1[:,i] - mfccs_2[:,j])
            dist[i][j] = euclidean


    #finding dynamic time warping
    #dtw = np.zeros(shape = (mfccs_1.shape[1], mfccs_2.shape[1]))
    #dtw[0][0] = dist[0][0]
    # for i in range(1,mfccs_1.shape[1]):
    #     for j in range(1,mfccs_2.shape[1]):
    #         dtw[i][j] = min(dtw[i-1][j-1], dtw[i-1][j], dtw[i][j-1]) + dist[i][j]
    dtw,_ = librosa.sequence.dtw(C = dist)

    #to normalise distance into a percentage
    mx = max(dtw.flatten())

    #percentage similarity
    print(dtw.shape[0], dtw.shape[1])
    res = '%.3f'%((mx - dtw[dtw.shape[0] - 1][dtw.shape[1] - 1]) / mx * 100)
    print(res, "%")
    return res

if __name__ == "__main__":
    filename_1 = input()
    filename_2 = input()
    _ = audio_comparator(file_1=filename_1, file_2=filename_2)
    