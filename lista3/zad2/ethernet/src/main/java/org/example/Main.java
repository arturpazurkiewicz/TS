package org.example;

import net.sourceforge.argparse4j.ArgumentParsers;
import net.sourceforge.argparse4j.inf.ArgumentParser;
import net.sourceforge.argparse4j.inf.ArgumentParserException;
import net.sourceforge.argparse4j.inf.Namespace;

public class Main {
    public static void main(String[] args) {
        ArgumentParser parser = ArgumentParsers.newFor("ethernet-1.0.jar").build()
                .description("Ethernet Simulation");
        parser.addArgument("-c", "--cableLength").help("Type wire length").type(Integer.class).setDefault(30);
        parser.addArgument("-r", "--router").help("Type router size").type(Integer.class).setDefault(5);
        parser.addArgument("-l", "--programLength").help("Type program iterations").setDefault(100000).type(Integer.class);
        parser.addArgument("-ifg", "--interframeGap").setDefault(2).help("Set interframe gap").type(Integer.class);
        parser.addArgument("-p", "--probability").setDefault(0.01).help("Set probability of sending\n").type(Double.class);
        try {
            Namespace cli = parser.parseArgs(args);
            int c = cli.get("cableLength");
            int r = cli.get("router");
            int l = cli.get("programLength");
            int ifg = cli.get("interframeGap");
            double p = cli.get("probability");

            Wire wire = new Wire(c);
            if (r > 0)
                wire.addRouter(new Router(1, 0, ifg, p, wire));
            if (r > 1)
                wire.addRouter(new Router(r, c - 1, ifg, p, wire));
            routerGenerator(c, r, ifg, p, wire);
            wire.generateMessageSize();
            int counter = 0;
            for (int i = 0; i < l; i++) {
                counter++;
                System.out.println(wire + " " + counter);
                wire.doMove();
            }
            System.out.println("Valid " + wire.valid + " Invalid " + wire.invalid);
        } catch (ArgumentParserException e) {
            parser.handleError(e);
        }
    }

    private static void routerGenerator(int c, int r, int ifg, double p, Wire wire) {
        for (int i = 2; i < r && i < c; i++) {
            while (true) {
                int a = (int) (Math.random() * (c - 2)) + 1;
                if (wire.wireCable[a].charAt(0) != 'r') {
                    wire.addRouter(new Router(i, a, ifg, p, wire));
                    break;
                }
            }
        }
    }
}

