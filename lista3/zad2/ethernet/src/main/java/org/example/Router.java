package org.example;

import javax.swing.*;
import java.util.ArrayList;
import java.util.jar.JarOutputStream;

public class Router {
    enum OperatingMode {
        SendingMessage, Listening, WaitingAfterError, SendingError, WaitingForErrorEnd
    }

    private int mainTimer = 0;
    private int errorCounter = 1;
    private int position;
    private Wire wire;
    private final int id;
    private OperatingMode mode = OperatingMode.Listening;
    private ArrayList<Message> messages;
    private boolean wantsSend = false;
    private int t;
    private final int ifg_o;
    private int ifg = 0;
    private final double sendProbability;


    public Router(int id, int position, int ifg, double sendProbability, Wire wire) {
        messages = new ArrayList<>();
        this.id = id;
        this.position = position;
        this.wire = wire;
        this.t = Math.max(position, wire.length - 1 - position);
        wire.writeToCable(position,"r"+id);
        this.ifg_o = ifg;
        this.sendProbability = sendProbability;
    }

    public void sendMessage() {
        System.out.println("Router " + id + " is sending message");
        messages.add(new Message("m" + id, position, 2 * t, wire, Message.Direction.Both));
        mainTimer = 2 * t;
        wantsSend = false;
        ifg = ifg_o;
    }

    public void sendErrorMessage() {
        wire.invalid++;
        System.out.println("Router " + id + " is sending error");
        messages.add(new Message("e" + id, position, wire.length, wire, Message.Direction.Both));
        mainTimer += 2 * t;
        ifg = ifg_o;
    }

    public int getPosition() {
        return position;
    }

    public int getId() {
        return id;
    }

    public void doMovePreparations() {
        for (int i = messages.size() - 1; i > -1; i--) {
            if (messages.get(i).isDead()) {
                messages.remove(i);
            } else {
                messages.get(i).move();
            }
        }
    }

    public void doMove() {
        int isFree = wire.isCableFree(position);
        if (mode == OperatingMode.WaitingForErrorEnd && isFree != -1)
            mode = OperatingMode.WaitingAfterError;
        if (mode != OperatingMode.WaitingForErrorEnd)
            mainTimer--;


        if (mainTimer < 1) {
            if (mode == OperatingMode.SendingMessage) {
                System.out.println("Router " + id + " has successfully sent message");
                wire.valid++;
                errorCounter = 1;
            }
            mode = OperatingMode.Listening;
        }
        if (isFree == 0 && mode != OperatingMode.SendingMessage && mode != OperatingMode.SendingError){
            ifg--;
        } else {
            ifg = ifg_o;
        }

        switch (mode) {
            case WaitingAfterError:
            case SendingError:
                break;
            case SendingMessage:
                switch (isFree) {
                    case 0:
                        break;
                    case 1:
                        handleError();
                        wantsSend = true;
                        sendErrorMessage();
                        break;
                    default:
                        System.out.println("Router " + id + " received error");
                        handleError();
                }
                break;
            case Listening:
                if ((ifg < 1 && (Math.random() <= sendProbability)) || (wantsSend && ifg < 1)) {
                    sendMessage();
                    mode = OperatingMode.SendingMessage;
                }
//                    System.out.println("Listening");
                break;
        }

    }

    private void handleError() {
        messages.forEach(Message::stop_sending);
        if (errorCounter > 15) {
            System.out.println("Could not connected "+ id);
        }
        int e = Math.min(errorCounter, 10);
        mainTimer = (int) (Math.pow(2, e) * Math.random()) * (t + ifg_o) * 2;
        mode = OperatingMode.WaitingAfterError;
        errorCounter++;
        System.out.println("Router " + id + " waits " + mainTimer);
    }

    public void setT(int t) {
        this.t = t;
    }
}
