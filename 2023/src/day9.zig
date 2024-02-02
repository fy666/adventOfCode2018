const std = @import("std");
const ascii = @import("std").ascii;
const utils = @import("./utils.zig");

const fileData = @embedFile("./files/day9.txt");
const fileDataEx = @embedFile("./files/day9ex.txt");

fn diff(data: *std.ArrayList(i64)) void {
    var window = std.mem.window(i64, data.items, 2, 1);
    var ix: usize = 0;
    while (window.next()) |it| : (ix += 1) {
        //std.debug.print("{} {any}\n", .{ ix, it });
        data.items[ix] = it[1] - it[0];
    }

    _ = data.pop();
}

fn all_zeroes(data: *const std.ArrayList(i64)) bool {
    //std.debug.print("Type of data = {s}\n", .{@typeName(@TypeOf(data))});
    for (data.items) |item| {
        if (item != 0) {
            return false;
        }
    }
    return true;
}

fn predict(data: *std.ArrayList(i64)) [2]i64 {
    var sum_last: i64 = data.getLast();
    var sum_first: i64 = data.items[0];
    var ix: i64 = 0;
    while (!all_zeroes(data)) : (ix += 1) {
        diff(data);
        sum_last += data.getLast();
        if (@mod(ix, 2) == 0) {
            sum_first -= data.items[0];
        } else {
            sum_first += data.items[0];
        }
        //std.debug.print("{any} ->", .{data.items});
    }
    return .{ sum_last, sum_first };
}

fn solve(data: anytype) !void {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();
    var splits = std.mem.split(u8, data, "\n");
    var summed_score_part1: i64 = 0;
    var summed_score_part2: i64 = 0;
    while (splits.next()) |line| {
        var numbers = std.ArrayList(i64).init(allocator);
        try utils.get_all_numbers(i64, line, &numbers);
        //std.debug.print("{any} -> ", .{numbers.items});
        var tmp: [2]i64 = predict(&numbers);
        //std.debug.print("  => {d}\n", .{tmp});
        summed_score_part1 += tmp[0];
        summed_score_part2 += tmp[1];
    }

    std.debug.print("Part 1 = {}, Part 2 = {}\n", .{ summed_score_part1, summed_score_part2 });
}

pub fn main() !void {
    const argv = std.os.argv;
    var example: bool = false;
    std.log.info("Hello day 9: {s}", .{argv});
    for (argv) |args| {
        if (std.mem.eql(u8, args[0..2], "ex")) {
            example = true;
        }
    }
    try solve(if (example) fileDataEx else fileData);
}
