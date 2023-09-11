#!/usr/bin/perl

use strict;
use warnings;
use utf8;  # Enable Unicode handling
use open qw(:std :utf8);  # Set UTF-8 encoding for input/output streams

# Script to display emoji from the specified range with hex codes and indices

if (@ARGV != 2) {
    die "Usage: $0 <start_hex_code> <count>\n";
}

my $emojiRangeStart = hex($ARGV[0]);
my $count = $ARGV[1];

for (my $i = 0; $i < $count; $i++) {
    my $emojiCode = $emojiRangeStart + $i;
    my $emojiChar = chr($emojiCode);
    my $hexCode = sprintf("%X", $emojiCode);
    print "$i: $emojiChar ($hexCode) ";
}

print "\n";
