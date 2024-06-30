import plotly.graph_objects as go
import numpy as np #ver < 2.0, kaleido
import librosa 
import IPython.display as ipd
import matplotlib.pyplot as plt
import os 
import librosa.display
import tqdm

def plot_fft(data, xt, notes, dimensions=(960,540), MINIMUM_FREQ = 10, MAXIMUM_FREQ = 1500):
  layout = go.Layout(
      title="frequency spectrum",
      autosize=False,
      width=dimensions[0],
      height=dimensions[1],
      xaxis_title="Frequency (note)",
      yaxis_title="Magnitude",
      font={'size' : 24}
  )

  fig = go.Figure(layout=layout,
                  layout_xaxis_range=[MINIMUM_FREQ, MAXIMUM_FREQ],
                  layout_yaxis_range=[0,1]
                  )
  
  fig.add_trace(go.Scatter(
      x = xt,
      y = data))
  
  for note in notes:
    fig.add_annotation(x=note[0]+10, y=note[2],
            text=note[1],
            font = {'size' : 48},
            showarrow=False)
  return fig

def extract_sample(audio, frame_number, FRAME_OFFSET, FFT_WINDOW):
  end = frame_number * FRAME_OFFSET
  begin = int(end - FFT_WINDOW)

  if end == 0:
    # We have no audio yet, return all zeros (very beginning)
    return np.zeros((np.abs(begin)),dtype=float)
  elif begin<0:
    # We have some audio, pad them with zeros
    return np.concatenate([np.zeros((np.abs(begin)),dtype=float),audio[0:end]])
  else:
    # return the next sample
    return audio[begin:end]

def find_top_notes(fft,num, xf, NOTES):
  if np.max(fft.real)<0.001:
    return []

  lst = [x for x in enumerate(fft.real)]
  lst = sorted(lst, key=lambda x: x[1],reverse=True)

  idx = 0
  found = []
  found_note = set()
  while( (idx<len(lst)) and (len(found)<num) ):
    f = xf[lst[idx][0]]
    y = lst[idx][1]
    n = freq_to_number(f)
    n0 = int(round(n))
    name = note_name(n0, NOTES=NOTES)

    if name not in found_note:
      found_note.add(name)
      s = [f,note_name(n0, NOTES=NOTES),y]
      found.append(s)
    idx += 1
    
  return found

def freq_to_number(f): return 69 + 12*np.log2(f/440.0)
def number_to_freq(n): return 440 * 2.0**((n-69)/12.0)
def note_name(n, NOTES): return NOTES[n % 12] + str(int(n/12 - 1))



def extractor(filepath : str):
  # Declare constants
  FPS = 30
  EK_WINDOW = 0.5
  MINIMUM_FREQ = 10
  MAXIMUM_FREQ = 1500
  DOMINANT_NOTES = 3
  NOTES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"] # C MAJOR SCALE
  RES = (1920, 1080)
  SCALE = 2
  # File path and loading
  raw_audio, sr = librosa.load(filepath)
  # Framing and Sampling
  FRAME_SAMPLES = (sr / FPS) # no of audio samples in one frame
  FFT_WINDOW = int(sr * EK_WINDOW)
  AUDIO_LEN = len(raw_audio) / sr
  # Hanning window function
  window = 0.5 * (1 - np.cos(np.linspace(0, 2*np.pi, FFT_WINDOW, False)))

  xf = np.fft.rfftfreq(FFT_WINDOW, 1/sr)
  FRAME_COUNT = int(AUDIO_LEN*FPS)
  FRAME_OFFSET = int(len(raw_audio)/FRAME_COUNT)

  # find out the maximum amplitude so we can scale.
  mx = 0
  for frame_number in range(FRAME_COUNT):
    sample = extract_sample(raw_audio, frame_number, FRAME_OFFSET=FRAME_OFFSET, FFT_WINDOW=FFT_WINDOW)

    fft = np.fft.rfft(sample * window)
    fft = np.abs(fft).real 
    mx = max(np.max(fft),mx)

  print(f"Max amplitude: {mx}")

  # Pass 2, produce the animation
  for frame_number in tqdm.tqdm(range(FRAME_COUNT)):
    sample = extract_sample(raw_audio, frame_number, FRAME_OFFSET=FRAME_OFFSET, FFT_WINDOW=FFT_WINDOW)

    fft = np.fft.rfft(sample * window)
    fft = np.abs(fft) / mx 
      
    s = find_top_notes(fft,DOMINANT_NOTES, xf=xf, NOTES=NOTES)

    fig = plot_fft(fft.real,xf,s,RES, MINIMUM_FREQ=MINIMUM_FREQ, MAXIMUM_FREQ=MAXIMUM_FREQ)
    fig.write_image(f"content\\frame{frame_number}.png",scale=2)


if __name__ == "__main__":
  while True:
    try:
      filepath = input()
      extractor(filepath=filepath)
    except Exception as e:
      print("either the file doesn't exist, or the path isn't correct or the format isn't compatible.")