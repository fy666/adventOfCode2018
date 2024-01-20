const std = @import("std");
const ascii = @import("std").ascii;
const utils = @import("./utils.zig");

const fileData = @embedFile("./files/day24.txt");
const fileDataEx = @embedFile("./files/day24ex.txt");

const Regex = @import("zig-regex").Regex;

const Allocator = std.mem.Allocator;
fn line_intersect(comptime T: type, x1: T, y1: T, x2: T, y2: T) bool {
    if (x1 >= x2 and y1 <= y2) {
        return true;
    }
    if (x2 >= x1 and y2 <= y1) {
        return true;
    }
    if (x1 <= y2 and y1 >= y2) {
        return true;
    }
    if (x2 <= y1 and y2 >= y1) {
        return true;
    }
    return false;
}
const Stone = struct {
    name: []const u8,
    pos: [3]i64,
    speed: [3]i64,

    pub fn init(name: []const u8) Stone {
        return Stone{ .name = name, .pos = [3]i64{ 0, 0, 0 }, .speed = [3]i64{ 0, 0, 0 } };
    }

    pub fn intersect(self: Stone, other: Stone) bool {
        _ = other;
        _ = self;
        //TODO
        return true;
        //return line_intersect(u32, self.p1[0], self.p2[0], other.p1[0], other.p2[0]) and line_intersect(u32, self.p1[1], self.p2[1], other.p1[1], other.p2[1]);
    }
};

fn printStringHashMap(data: std.StringHashMap(bool)) void {
    var it = data.iterator();
    while (it.next()) |item| {
        std.debug.print("{s},", .{item.key_ptr.*});
    }
}

fn parse_stone(
    line: []const u8,
    counter: usize,
    allocator: Allocator,
    stones: *std.ArrayList(Stone),
) !void {
    var re = try Regex.compile(allocator, "(\\d+), (\\d+), (\\d+) @ ([0-9-]+), ([0-9-]+), ([0-9-]+)");
    var captures = try re.captures(line);
    if (captures != null) {
        var stone = Stone.init(try std.fmt.allocPrint(allocator, "{}", .{counter}));
        for (0..3) |ix| {
            stone.pos[ix] = try std.fmt.parseInt(i64, captures.?.sliceAt(ix + 1).?, 10);
            stone.speed[ix] = try std.fmt.parseInt(i64, captures.?.sliceAt(ix + 4).?, 10);
        }
        try stones.append(stone);
    } else {
        std.debug.print("{s} not found\n", .{line});
        unreachable;
    }
}

fn solve(data: anytype) !void {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();

    var splitsLines = std.mem.split(u8, data, "\n");

    var stones = std.ArrayList(Stone).init(allocator);
    var counter: usize = 0;
    while (splitsLines.next()) |l| : (counter += 1) {
        try parse_stone(l, counter, allocator, &stones);
    }

    std.debug.print("{} stones found \n", .{stones.items.len});
}

pub fn main() !void {
    const argv = std.os.argv;
    var example: bool = false;
    std.log.info("Hello day 24: {s}", .{argv});
    for (argv) |args| {
        if (std.mem.eql(u8, args[0..2], "ex")) {
            example = true;
        }
    }

    try solve(if (example) fileDataEx else fileData);
}
