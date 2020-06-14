package org.example;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.Comparator;

public class Wire {
    String[] wireCable;
    private ArrayList<Router> routers;
    public int length;
    private int message_length = 1;
    private boolean reverse = true;
    public int valid = 0;
    public int invalid = 0;


    public Wire(int length) {
        routers = new ArrayList<>();
        wireCable = new String[length];
        for (int i = 0; i < length; i++) {
            wireCable[i] = "  ";
        }
        this.length = length;
        this.message_length = 2 * length;
    }

    public int isCableFree(int position) {
        switch (wireCable[position].charAt(0)) {
            case ' ':
            case 'r':
                return 0;
            case 'm':
                return 1;
            default:
                return -1;
        }
    }

    public int getMessage_length() {
        return message_length;
    }

    public void writeToCable(int position, String message) {
        try {
            wireCable[position] = message;
        } catch (ArrayIndexOutOfBoundsException ignore) {
        }
    }

    public void addRouter(Router router) {
        routers.add(router);
    }

    @Override
    public String toString() {
//        for (Router router : routers) {
//            if (wireCable[router.getPosition()].equals("  "))
//                wireCable[router.getPosition()] = "r" + router.getId();
////            r.append(router.getOperatingMode()).append(" ").append(router.getTimer());
//        }

        return Arrays.toString(wireCable);
    }

    public void freeCable(int position, String info) {
        try {
            if (wireCable[position].compareTo(info) == 0)
                wireCable[position] = "  ";
        } catch (ArrayIndexOutOfBoundsException ignore) {
        }
    }

    public void doMove() {
        wireCable = new String[length];
        for (int i = 0; i < length; i++) {
            wireCable[i] = "  ";
        }
        if (reverse) {
            for (Router value : routers) {
                value.doMovePreparations();
            }
        } else {
            for (int i = routers.size() - 1; i >= 0; i--) {
                routers.get(i).doMovePreparations();
            }
        }

        for (Router router : routers) {
            if (wireCable[router.getPosition()].equals("  "))
                wireCable[router.getPosition()] = "r" + router.getId();
            router.doMove();
        }
        reverse = !reverse;
    }

    public void generateMessageSize() {
        routers.sort(new Comparator<Router>() {
            @Override
            public int compare(Router o1, Router o2) {
                return o1.getPosition() - o2.getPosition();
            }
        });
        message_length = routers.get(routers.size()-1).getPosition() - routers.get(0).getPosition() + 1;
        if (message_length == 1)
            message_length = length;
        for (Router router : routers)
            router.setT(message_length);
    }

}
