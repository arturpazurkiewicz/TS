package org.example;

public class Message {
    enum Direction {
        Left, Right, Both
    }

    private final Direction direction;
    private final String info;
    private int length;
    private int actual_length;
    private int actual_positionL;
    private int actual_positionR;
    private int timer;
    private Wire wire;

    public Message(String info, int startingPosition, int length, Wire wire, Direction direction) {
        this.info = info;
        this.length = length;
        this.wire = wire;
        this.actual_length = 1;
        this.actual_positionL = this.actual_positionR = startingPosition;
        this.direction = direction;
        this.timer =2 * length;
        move();
    }

    public void stop_sending(){
        length = actual_length;
    }

    public void writePomR(int end){
        for (int i = 0; i < actual_length -1; i++) {
            wire.writeToCable(end-i, info);
        }
    }

    public void writePomL(int end){
        for (int i = 0; i < actual_length -1; i++) {
            wire.writeToCable(end+i, info);
        }
    }

    public void move() {
        timer --;
        if (direction == Direction.Right || direction == Direction.Both) {
            writePomR(actual_positionR);
            actual_positionR++;

        }
        if (direction == Direction.Left || direction == Direction.Both) {
            if (actual_length <= length) {
                writePomL(actual_positionL);
            } else {
                writePomL(actual_positionL);
//                wire.freeCable(actual_positionL + actual_length -1, info);
            }
            actual_positionL--;

        }
        if (actual_length <= length)
            actual_length++;
    }
    public boolean isDead(){
        return timer < 1;
    }
}
