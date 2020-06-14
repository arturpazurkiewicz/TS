#!/usr/bin/python3
import libscrc
import argparse

FLAG = '01111110'


def gen_crc(data, size):
    if size < 64:
        crc = bin(libscrc.crc8(bytes(data, 'ascii')))[2:].zfill(8)
    elif size < 16384:
        crc = bin(libscrc.tcp(bytes(data, 'ascii')))[2:].zfill(16)
    else:
        crc = bin(libscrc.crc32(bytes(data, 'ascii')))[2:].zfill(32)
    return crc


def slice_to_frames(d, size):
    r = []
    while len(d) > 0:
        a = d[:size - 1]
        d = d[len(a):]
        r.append(a)
    return r


def encode(d):
    frames = slice_to_frames(d, frame_size)
    result = ""
    for frame in frames:
        result += FLAG + frame_stuffing(frame + gen_crc(frame, frame_size),
                                        5) + FLAG
    return result


def decode(data):
    if not (data.endswith(FLAG) and data.startswith(FLAG)):
        print('Invalid frame')
        exit(0)
    d = data.split(FLAG)
    result = ""
    for i in range(len(d)):
        if i % 2 == 1:
            frame = frame_unstuffing(d[i], 5)
            l = len(frame)
            if l < 72:
                size1 = 8
            elif l < 16400:
                size1 = 16
            else:
                size1 = 32
            size1_t = -1 * size1
            data1 = frame[:size1_t]
            verify1 = frame[size1_t:]
            if verify1 != gen_crc(data1, size1):
                print('Invalid data')
                exit(0)
            result += data1
    return result


def frame_stuffing(data, stuffing_treshold):
    return data.replace('1' * stuffing_treshold, '1' * stuffing_treshold + '0')


def frame_unstuffing(data, stuffing_treshold):
    return data.replace('1' * stuffing_treshold + '0', '1' * stuffing_treshold)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--type", help="encode or decode",
                        choices=["encode", "decode", "test"],
                        default="encode")
    parser.add_argument("-i", "--input", help="input file",
                        default="input.txt")
    parser.add_argument("-o", "--output", help="output file",
                        default="output.txt")
    parser.add_argument("-m", "--max", help="max frame size", default="62")
    args = parser.parse_args()

    frame_size = 32
    with open(args.input, 'r') as f:
        data = f.read()

    if args.type == 'test':
        print('data   ', data)
        e = encode(data)
        print('encoded', e)
        d = decode(e)
        print('decoded', d)
        print('Are the same: ',d == data)
    else:
        if args.type == 'decode':
            result = decode(data)
        else:
            result = encode(data)
        with open(args.output, 'w') as f:
            f.write(result)
