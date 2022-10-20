# ML Methods for Side Channel Analysis

Adding experiments and interesting stuff here with time.

#### Currently:

- This solves the old AES Templating tutorial in CW wiki by creating a ML model for predicting the key
    - only works for fixed plaintext
    - One GB of compressed traces in `traces.7z`

Annotated output:
```
Demo from disk?y       # <- Uses pre-recrded traces from the 7z, fixed text
0 0.9996618194115657   # <- Score per key byte
1 0.9996618194115657
2 0.9976327358809605
3 0.9986472776462632
4 0.9913763949949272
5 0.9976327358809605
6 0.9986472776462632
7 0.9974636455867433
8 0.9876564085221509
9 0.9981400067636118
10 0.9959418329387894
11 0.9993236388231316
12 0.9925600270544471
13 0.9972945552925262
14 0.9979709164693946
15 0.9979709164693946
[0.9996618194115657, 0.9996618194115657, .....  # <- Prints all the final scores
41 86 a1 3f 62 06 5b 9a 6c 97 24 de 0a 4c bd 3f # <- Connects to a ChipWhisperer and starts testing
41 86 a1 3f 62 06 5b 9a 48 97 24 de 0a 4c bd 3f
1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1
6b 91 ce 43 17 98 88 6b 99 5d ec e9 18 c3 09 88 # <- Keys in hex
6b 91 ce 43 17 98 88 6b 99 5d ec e9 18 c3 09 88
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1                 # <- Correctly guessed bytes
a1 23 b8 48 e8 a9 1e 1f 49 a8 87 81 d9 f6 e8 ee
a1 23 b8 48 e8 a9 1e 1f 49 a8 87 81 d8 f6 e8 cf
1 1 1 1 1 1 1 1 1 1 1 1 0 1 1 0
b0 fa 5e 25 34 fe 7f 71 ff 42 00 ed 53 48 3b 12
b0 fa 5e 25 34 fe 7f 71 ff 42 00 ed 53 48 3b 12
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
94 eb 75 fd 76 f5 17 70 27 68 c3 55 54 ec 37 8f
94 eb 75 fd 76 f5 17 70 27 68 c3 55 54 ec 37 8f
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
de 99 0d 84 46 6e 39 89 8e e0 47 a3 48 50 b3 07
de 99 0d 84 46 6e 39 89 8e cd 04 a3 48 50 b3 07
1 1 1 1 1 1 1 1 1 0 0 1 1 1 1 1                 # <- Will fail guessing sometimes
d5 d8 c4 65 2f 3d 9b 0f cb 74 cd 9e 57 8f f6 d9
d5 d8 c4 65 2f 3d 9b 0f cb 74 cd 9e 57 8f f6 d9
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
7f 2d a7 31 aa fa 02 15 b1 1f e3 f8 c8 db 2b 34
7f 2d a7 31 aa fa 02 15 b1 1f e3 f8 c8 db 2b 34
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
16 62 a0 76 52 5c bb 6d 91 60 79 fc 6b 59 9f 5a
16 62 a0 76 55 5c bb 6d 15 60 79 fc 6b 59 9f 5a
1 1 1 1 0 1 1 1 0 1 1 1 1 1 1 1
92 27 a0 e8 fc 02 8a 19 c5 d9 3f 4c 31 69 5a b4
92 27 a0 e8 fc 02 8a 19 c5 d9 3f 4c 31 69 5a 75
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
33 53 dd 9c 7f dd 15 bb 91 07 b9 d6 89 50 07 bc
33 53 dd 9c 7f dd 15 bb 91 07 b9 d6 89 50 07 bc
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
f4 fb 58 0d 58 65 e7 11 d2 ee 9c a6 4f a6 5c 96
f4 fb 58 0d 3d 65 e7 11 c3 ee 9c a6 4f a6 5c 28
1 1 1 1 0 1 1 1 0 1 1 1 1 1 1 0
da 9c f1 0b 93 b0 91 d0 ee dc 2d b7 8d e6 bb 33
da 9c f1 0b d1 b0 91 d0 de dc 2d b7 8d e6 bb 33
1 1 1 1 0 1 1 1 0 1 1 1 1 1 1 1
ec d0 f2 21 0f 5a f9 44 b7 32 c7 5c 5d e4 79 90
ec d0 f2 21 0f 5a f9 44 b7 32 c7 5c 5d aa 79 90
1 1 1 1 1 1 1 1 1 1 1 1 1 0 1 1
58 08 19 e7 92 62 08 b3 ef ee 26 64 b0 25 a7 39
58 08 19 e7 92 62 08 b3 ef ee 26 64 b0 25 a7 39
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
7e d8 2a c3 99 63 63 12 f3 3c 92 8b a1 ae 50 48
7e d8 2a c3 99 63 63 12 f3 3c 92 8b a1 ae 50 48
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
33 e7 fb 7f 87 df 83 ff 70 47 00 ac c6 f3 4a e3
33 e7 fb 7f 87 df 83 ff 70 47 00 ac c6 f3 4a e3
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
5f 4b 2f 55 53 95 7d cc 47 68 a0 e5 53 22 b4 8d
5f 4b 2f 55 53 95 7d cc 47 68 a0 e5 53 22 b4 8d
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
16 e9 24 51 96 78 21 7c 41 04 30 00 df 7c 96 c7
16 e9 24 51 96 78 21 7c 41 04 30 00 df 7c 96 df
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
41 3e 9f 60 5a 85 07 3c a9 9f e6 a0 7c c1 b0 cf
41 3e 9f 60 5a 85 07 3c a9 9f e6 11 7c c1 b0 cf
1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1
fc a5 87 22 9a e6 fb bc b5 11 f1 41 35 b6 b1 f1
fc a5 87 22 9a e6 fb f9 a7 11 f1 41 35 d6 ed f1
1 1 1 1 1 1 1 0 0 1 1 1 1 0 0 1
59 60 c0 98 31 31 1d 1e 2a fe 13 23 11 c2 c2 1d
59 60 c0 98 31 31 1d 1e 2a fe 13 23 1d 83 c2 1d
1 1 1 1 1 1 1 1 1 1 1 1 0 0 1 1
38 c1 10 50 23 5f c5 8a 8c 79 bd 8f 50 f6 65 dc
38 c1 10 50 23 5f c5 8a 8c 79 bd 8f 50 f6 65 dc
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
74 28 ab 43 c6 4b e1 50 e7 9b 22 98 67 fa ab 85
74 28 ab 43 c6 4b e1 50 e7 9b 22 98 67 fa ab 85
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
b9 fc 6c f3 31 66 04 84 1a 1c 3c 3b 34 17 d7 a1
b9 fc 6c f3 31 66 04 84 1a 1c 3c 3b 34 17 d7 a1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
87 f4 e7 ae 6a 6c d7 9b 85 ed 32 88 6e 60 e3 ec
87 f4 e7 ae 6a 6c d7 9b 85 ed 32 88 6e 60 e3 ec
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
4b 39 cd 0c d9 d9 d1 f7 ce ea 15 c3 6e ce 04 7b
4b 39 cd 0c d9 d9 d1 f7 ce ea 15 c3 6e ce 04 7b
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
b3 51 d4 f4 32 79 37 f1 c2 08 a9 f3 5f d7 ff 25
b3 51 d4 f4 32 79 37 f1 c2 08 a9 f3 5f d7 ff 25
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
d1 7a cc 5b a6 f4 7a 61 6d 8b 92 9a d7 ea 4d ed
d1 7a cc 5b d4 f4 7a 61 6d 8b 92 9a e2 ea 4d ed
1 1 1 1 0 1 1 1 1 1 1 1 0 1 1 1
2b d2 b7 c9 04 e4 ea ec 17 65 4c e8 d8 31 de 43
2b d2 b7 c9 04 e4 ea bd 17 65 6c e8 d8 31 de 43
1 1 1 1 1 1 1 0 1 1 0 1 1 1 1 1
65 58 8b 5d 80 25 57 e3 43 01 d2 15 c7 84 43 99
65 58 8b 5d 80 25 57 e3 42 01 d2 15 c7 84 43 99
1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1
93 cd 92 c0 01 04 46 5b 45 c6 70 5c 71 24 a6 38
93 cd 92 c0 01 04 46 5b 45 c6 70 5c 71 24 a6 11
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
53 3d 40 c3 08 f7 29 71 5e a3 cd 6e 22 70 59 4b
53 3d 40 c3 08 f7 29 71 5e a3 cd 4f 22 70 59 4b
1 1 1 1 1 1 1 1 1 1 1 0 1 1 1 1
e5 3f 7b e1 e3 c1 15 e9 ad ba 9d 8d 5b 1d 9a 49
e5 3f 7b e1 e3 c1 15 e9 ad ba 9d 8d 5b 1d 9a 49
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
2f 47 e9 d9 60 04 d3 e6 be 51 b9 5c f0 cf 69 d9
2f 47 e9 d9 60 04 d3 e6 ca 51 b9 5c f0 cf 69 d9
1 1 1 1 1 1 1 1 0 1 1 1 1 1 1 1
```