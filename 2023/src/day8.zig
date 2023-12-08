const std = @import("std");
const ascii = @import("std").ascii;
const utils = @import("./utils.zig");

const fileData = @embedFile("./files/day8.txt");
const fileDataEx = @embedFile("./files/day8ex.txt");
const Regex = @import("zig-regex").Regex;

const Allocator = std.mem.Allocator;

fn fill_hashmap(line: []const u8, hashmap: anytype) !void {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();
    var re = try Regex.compile(allocator, "(\\w+) = ((\\w+),(\\w+))");

    var captures = try re.captures(line);
    //std.debug.print("captures = {}\n", .{captures.?.len()});
    if (captures != null) {
        //AAA = (BBB, CCC)
        var map = Map{ .left = captures.?.sliceAt(2), .right = captures.?.sliceAt(3) };
        std.debug.print("map L={}, R={}", .{ map.left, map.right });
        try hashmap.put(captures.?.sliceAt(2), map);
    }
}

pub const Map = struct {
    left: [3]u8,
    right: [3]u8,
};

fn solve(data: anytype) !void {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();
    var network = std.AutoHashMap([3]u8, Map).init(allocator);
    var commands: *[]u8 = null;
    var splits = std.mem.split(u8, data, "\n\n");
    var ix: i32 = 0;
    while (splits.next()) |line| : (ix += 1) {
        if (ix == 0) {
            commands = line;
            continue;
        }
        var map_lines = std.mem.split(u8, line, "\n");
        while (map_lines.next()) |l| {
            fill_hashmap(l, &network);
        }
    }

    std.debug.print("Part 2 = {}\n", .{42});
}

pub fn main() !void {
    const argv = std.os.argv;
    var example: bool = false;
    std.log.info("Hello day 8: {s}", .{argv});
    for (argv) |args| {
        if (std.mem.eql(u8, args[0..2], "ex")) {
            example = true;
        }
    }
    try solve(if (example) fileDataEx else fileData);
}
