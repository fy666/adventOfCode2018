const std = @import("std");
const ascii = @import("std").ascii;

const fileData = @embedFile("./files/day4.txt");
const fileDataEx = @embedFile("./files/day4ex.txt");
const Regex = @import("zig-regex").Regex;

fn get_match(line: []const u8) !?i32 {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();
    var re = try Regex.compile(allocator, "(\\d+)");

    var captures = try re.captures(line);
    var result: ?i32 = null;
    //std.debug.print("captures = {}\n", .{captures.?.len()});
    if (captures != null) {
        var cap = captures.?.sliceAt(1);
        result = try std.fmt.parseInt(i32, cap.?, 10);
    }
    return result;
}

fn get_all_numbers(line: []const u8, values: *std.ArrayList(i32)) !void {
    var split_numbers = std.mem.split(u8, line, " ");
    while (split_numbers.next()) |num_str| {
        var res = try get_match(num_str);
        if (res != null) {
            try values.append(res.?);
            //std.debug.print("{s} -> {} \n", .{ num_str, res.? });
        }
    }
    //std.debug.print("{s} -> {any} \n", .{ line, values.items });
}

fn solve(data: anytype) !void {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();

    var sum_part1: i32 = 0;

    var game_hash = std.AutoHashMap(i32, i32).init(allocator);

    var game_num: i32 = 1;
    var splits = std.mem.split(u8, data, "\n");
    while (splits.next()) |line| : (game_num += 1) {
        var remove_game = std.mem.split(u8, line, ":");
        var game = remove_game.next();
        var numbers = remove_game.next().?;

        var split_numbers = std.mem.split(u8, numbers, "|");
        var winning_numbers = std.ArrayList(i32).init(allocator);
        try get_all_numbers(split_numbers.next().?, &winning_numbers);
        var drawn_numbers = std.ArrayList(i32).init(allocator);
        //std.debug.print("Winning = {any}\n", .{winning_numbers.items});
        try get_all_numbers(split_numbers.next().?, &drawn_numbers);
        //std.debug.print("Number list {s} -> ", .{numbers});
        std.debug.print("Winning = {any}, Drawn = {any}\n", .{ winning_numbers.items, drawn_numbers.items });
        var winning_drawn_numbers: i32 = 0;
        for (drawn_numbers.items) |drawn| {
            //if (std.mem.containsAtLeast(u32, &my_arr, 1, &[_]u32{42})) {

            if (std.mem.containsAtLeast(i32, winning_numbers.items, 1, &[_]i32{drawn})) {
                std.debug.print("{} is winning\n", .{drawn});
                winning_drawn_numbers += 1;
            }
        }
        try game_hash.put(game_num, winning_drawn_numbers);
        if (winning_drawn_numbers > 0) {
            var score = std.math.pow(i32, 2, winning_drawn_numbers - 1);
            std.debug.print("{s} -> {} winners -> score {}\n", .{ game.?, winning_drawn_numbers, score });
            sum_part1 += std.math.pow(i32, 2, winning_drawn_numbers - 1);
        }
    }

    // part 2
    var cards = std.ArrayList(i32).init(allocator);
    var ig: i32 = 1;
    while (ig < game_num) : (ig += 1) {
        try cards.append(ig);
    }

    var num_cards: i32 = 0;
    while (true) {
        num_cards += @intCast(cards.items.len);
        var new_cards = std.ArrayList(i32).init(allocator);
        // if all cards are not winning, exit
        var none_winning: bool = true;
        for (cards.items) |card| {
            var extra_cards: i32 = game_hash.get(card).?;
            if (extra_cards > 0) {
                none_winning = false;
            }
            var ix: i32 = 1;
            while (ix <= extra_cards) : (ix += 1) {
                try new_cards.append(card + ix);
            }
        }
        //std.debug.print("Start = {any}, drawn cards = {any}\n", .{ cards.items, new_cards.items });
        if (none_winning) {
            break;
        } else {
            cards = new_cards;
        }
    }

    var it = game_hash.iterator();
    while (it.next()) |item| {
        std.debug.print("{any} -> {any}\n", .{ item.key_ptr.*, item.value_ptr.* });
    }
    std.debug.print("Part 1 = {}, Part 2 = {}\n", .{ sum_part1, num_cards });
}

pub fn main() !void {
    const argv = std.os.argv;
    var example: bool = false;
    std.log.info("Hello day 4: {s}", .{argv});
    for (argv) |args| {
        if (std.mem.eql(u8, args[0..2], "ex")) {
            example = true;
        }
    }

    try solve(if (example) fileDataEx else fileData);
}
