const std = @import("std");
const ascii = @import("std").ascii;
const utils = @import("./utils.zig");

const fileData = @embedFile("./files/day12.txt");
const fileDataEx = @embedFile("./files/day12ex.txt");

fn get_combi(input: []const u8, groups: std.ArrayList(i32), hash: *std.StringHashMap(i64)) !i64 {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();
    const hash_input = try std.fmt.allocPrint(
        allocator,
        "{s} {any}",
        .{ input, groups.items },
    );
    if (hash.contains(hash_input) == true) {
        return hash.get(hash_input).?;
    }
    //std.debug.print("GET COMBI {s} and {any} \n", .{ input, groups.items });
    if (groups.items.len == 0) {
        if (std.mem.count(u8, input, "#") == 0) {
            //std.debug.print("Found a valid comb\n", .{});
            //try hash.put(hash_input, 1);
            return 1;
        }
        //try hash.put(hash_input, 0);
        return 0;
    }

    var num_hash: i32 = 0;
    for (groups.items) |x| {
        num_hash += x;
    }

    // Impossible to go further
    if (std.mem.count(u8, input, "#") + std.mem.count(u8, input, "?") < num_hash) {
        //std.debug.print("This combination cannot be correct, abort\n", .{});
        //try hash.put(hash_input, 0);
        return 0;
    }

    if (input[0] == '.') {
        var res = try get_combi(input[1..], groups, hash);
        //try hash.put(hash_input, res);
        return res;
    }

    var possibilities: i64 = 0;

    if (input[0] == '?') {
        possibilities += try get_combi(input[1..], groups, hash);
    }

    // Try to add first group

    var end_of_group_index: usize = @intCast(groups.items[0]);
    // Exact match
    if (input.len == end_of_group_index) {}
    if ((input.len == end_of_group_index) or
        ((input.len > end_of_group_index) and input[end_of_group_index] != '#'))
    {
        //std.debug.print("{s} and {any} -> enough space for 1st group\n", .{ input, groups.items });
        // No separation
        if (std.mem.count(u8, input[0..end_of_group_index], ".") == 0) {
            if (input.len == end_of_group_index) {
                possibilities += 1; // exact match
            } else {
                var new_group = try groups.clone(); // create copy
                _ = new_group.orderedRemove(0);
                //std.debug.print("{s} and {any} -> First group found, continue\n", .{ input, groups.items });
                possibilities += try get_combi(input[(end_of_group_index + 1)..], new_group, hash);
            }
        }
    }
    try hash.put(hash_input, possibilities);
    return possibilities;
}

fn get_part2_inputs(input: []const u8) ![]const u8 {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();

    var new_input: []u8 = try allocator.alloc(u8, input.len * 5 + 4);
    var ix: usize = 0;
    for (0..5) |_| {
        for (input) |c| {
            new_input[ix] = c;
            ix += 1;
        }
        if (ix < new_input.len) {
            new_input[ix] = '?';
        }
        ix += 1;
    }

    return new_input;
}

fn get_part2_groups(groups: std.ArrayList(i32)) !std.ArrayList(i32) {
    var group_cpy = try groups.clone();
    for (0..4) |_| {
        for (groups.items) |c| {
            try group_cpy.append(c);
        }
    }
    return group_cpy;
}

fn solve(data: anytype) !void {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();

    var splits = std.mem.split(u8, data, "\n");
    var il: usize = 0;
    var part1: i64 = 0;
    var part2: i64 = 0;

    var timer = try std.time.Timer.start();
    //timer.start();
    while (splits.next()) |line| : (il += 1) {
        var groups = std.ArrayList(i32).init(allocator);
        var split_line = std.mem.split(u8, line, " ");
        var record = split_line.first();
        try utils.get_all_numbers(i32, split_line.next().?, &groups);
        var combi_hash = std.StringHashMap(i64).init(allocator);
        var ic: i64 = try get_combi(record, groups, &combi_hash);
        std.debug.print("{s} {any} -> PART 1 = {} possibilities\n", .{ record, groups, ic });

        timer.reset();
        var records_p2 = try get_part2_inputs(record);
        std.debug.print("P1 {} ns\n", .{timer.lap()});
        var groups_p2 = try get_part2_groups(groups);
        timer.reset();
        //combi_hash.clearRetainingCapacity();
        var combi_hash2 = std.StringHashMap(i64).init(allocator);
        std.debug.print("PART 2 = {s} ({any}) -> {} possibilities \n-----------------------\n", .{ records_p2, groups_p2.items, 0 });

        var ic2: i64 = try get_combi(records_p2, groups_p2, &combi_hash2);
        std.debug.print("P2 {} ns\n", .{timer.lap()});
        std.debug.print("PART 2 = {s} ({any}) -> {} possibilities \n-----------------------\n", .{ records_p2, groups_p2.items, ic2 });
        part1 += ic;
        part2 += ic2;
    }

    std.debug.print("Part 1 {}\n", .{part1});
    std.debug.print("Part 2 {}\n", .{part2});
}

pub fn main() !void {
    const argv = std.os.argv;
    var example: bool = false;
    std.log.info("Hello day 12: {s}", .{argv});
    for (argv) |args| {
        if (std.mem.eql(u8, args[0..2], "ex")) {
            example = true;
        }
    }
    // var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    // defer arena_state.deinit();
    // const allocator = arena_state.allocator();
    // var groups = std.ArrayList(i32).init(allocator);
    // try groups.append(42);
    // try groups.append(10);
    // std.debug.print("BEFORE {any}\n", .{groups.items});
    // try test_arg(groups);
    // std.debug.print("AFTER {any}\n", .{groups.items});
    // std.debug.print("{s}\n", .{try get_part2_inputs(".##")});
    // var g2 = try get_part2_groups(groups);
    // std.debug.print("{any}\n", .{g2.items});
    var timer = try std.time.Timer.start();
    try solve(if (example) fileDataEx else fileData);
    var dt: f32 = @floatFromInt(timer.lap());
    std.debug.print("Day 15 in {} s\n", .{dt / 1e9});
}
