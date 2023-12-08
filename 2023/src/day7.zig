const std = @import("std");
const utils = @import("./utils.zig");

const fileData = @embedFile("./files/day7.txt");
const fileDataEx = @embedFile("./files/day7ex.txt");

fn replaceJokers(handMap: *std.AutoHashMap(u8, i32)) !void {
    var num_jokers: i32 = handMap.get('J').?;
    _ = handMap.remove('J');

    var it = handMap.iterator();
    var more_reccurrent_key: u8 = undefined;
    var more_recurrent_element: i32 = 0;
    while (it.next()) |item| {
        if (item.value_ptr.* > more_recurrent_element) {
            more_recurrent_element = item.value_ptr.*;
            more_reccurrent_key = item.key_ptr.*;
        }
    }
    try handMap.put(more_reccurrent_key, more_recurrent_element + num_jokers);
}

fn getType(handMap: *std.AutoHashMap(u8, i32)) i32 {
    var items: u32 = handMap.count();
    if (items == 1) {
        return 7; // full
    }
    if (items == 2) {
        var it = handMap.valueIterator();
        while (it.next()) |val| {
            if (val.* == 1 or val.* == 4) {
                return 6; // Four of a kind
            }
            if (val.* == 2 or val.* == 3) {
                return 5;
            }
        }
    }
    if (items == 3) {
        // Three of a kind
        var it = handMap.valueIterator();
        while (it.next()) |val| {
            if (val.* == 3) {
                return 4; // Three of a kind
            }
            if (val.* == 2) {
                return 3; // Two pairs
            }
        }
    }
    if (items == 4) {
        return 2; // one pair
    }
    if (items == 5) {
        return 1; // all different
    }
    unreachable;
}

pub const Hand = struct {
    hand: []const u8,
    numeric_hand: [5]u8,
    bid: i32,
    rank: i32,
    pub fn newHand(hand: []const u8, bid: i32, part2: bool) !Hand {
        var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
        defer arena_state.deinit();
        const allocator = arena_state.allocator();
        var handClassifier = std.AutoHashMap(u8, i32).init(allocator);
        var ih: usize = 0;
        var numeric_hand_local: [5]u8 = [_]u8{ 0, 0, 0, 0, 0 };
        for (hand) |c| {
            // numeric hand
            var num: u8 = switch (c) {
                'A' => 14,
                'K' => 13,
                'Q' => 12,
                'J' => 11,
                'T' => 10,
                '9' => 9,
                '8' => 8,
                '7' => 7,
                '6' => 6,
                '5' => 5,
                '4' => 4,
                '3' => 3,
                '2' => 2,
                '1' => 1,
                else => unreachable,
            };
            if (part2 and num == 11) {
                num = 0; // "J" now has lower priority
            }
            numeric_hand_local[ih] = num;
            ih += 1;

            var entry = handClassifier.get(c);
            var new_value: i32 = 1;
            if (entry != null) {
                new_value = entry.? + 1;
            }
            try handClassifier.put(c, new_value);
        }

        if (part2) {
            // update joker to compute hand rank
            try replaceJokers(&handClassifier);
        }
        var rank = getType(&handClassifier);
        var item = Hand{ .hand = hand, .bid = bid, .rank = rank, .numeric_hand = numeric_hand_local };
        return item;
    }
};

// should return true if a < b :)
fn cmpFunc(context: void, a: Hand, b: Hand) bool {
    _ = context;
    if (a.rank != b.rank) {
        return a.rank < b.rank;
    }
    var index: usize = 0;
    while (index < 5) : (index += 1) {
        if (a.numeric_hand[index] != b.numeric_hand[index]) {
            return a.numeric_hand[index] < b.numeric_hand[index];
        }
    }
    return false;
    //unreachable;
}

fn solve(data: anytype, part2: bool) !void {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();
    var hands = std.ArrayList(Hand).init(allocator);
    var splits = std.mem.split(u8, data, "\n");

    while (splits.next()) |line| {
        var hand_content = std.mem.split(u8, line, " ");
        var tmp_hand = hand_content.next().?;
        var bid = try utils.get_match(i32, hand_content.next().?);
        var hand = try Hand.newHand(tmp_hand, bid.?, part2);
        try hands.append(hand);
        //std.debug.print("New Hand {s} {} ({})\n", .{ hand.hand, hand.bid, hand.rank });
    }
    std.sort.insertion(Hand, hands.items, comptime {}, comptime cmpFunc);
    var hand_rank: i32 = 1;
    var score: i32 = 0;
    for (hands.items) |hand| {
        //std.debug.print("{}: {s} {}\n", .{ hand_rank, hand.hand, hand.bid });
        score += hand_rank * hand.bid;
        hand_rank += 1;
    }
    std.debug.print("Part {s} = {}\n", .{ if (part2) "2" else "1", score });
}

pub fn main() !void {
    const argv = std.os.argv;
    var example: bool = false;
    std.log.info("Hello day 7: {s}", .{argv});
    for (argv) |args| {
        if (std.mem.eql(u8, args[0..2], "ex")) {
            example = true;
        }
    }

    try solve(if (example) fileDataEx else fileData, false);
    try solve(if (example) fileDataEx else fileData, true);
}
