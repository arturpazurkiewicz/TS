#!/usr/bin/perl
use HTTP::Daemon;
use HTTP::Response;
use HTTP::Status;

my $d = HTTP::Daemon->new(
        LocalAddr => 'localhost',
        LocalPort => 8004,
    ) || die;

print "Please contact me at: <URL:", $d->url, ">\n";


while (my $c = $d->accept) {
    while (my $request = $c->get_request) {
        print $request->as_string, "\n";
        my $response = HTTP::Response->new(200);
        $response->header("Content-Type" => "text/text");
        $response->content($request->as_string);
        $c->send_response($response);
    }
    $c->close;
    undef($c);
}