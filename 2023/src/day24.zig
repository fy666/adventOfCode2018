const std = @import("std");
const ascii = @import("std").ascii;
const utils = @import("./utils.zig");

const fileData = @embedFile("./files/day24.txt");
const fileDataEx = @embedFile("./files/day24ex.txt");

const Regex = @import("zig-regex").Regex;

const Allocator = std.mem.Allocator;

fn solve2x2(a: f64, b: f64, c: f64, d: f64, e: f64, f: f64) ?[2]f64 {
    //std.debug.print("Solving:\n {} {} | t0 | {} \n {} {} | t1 | {} \n", .{ a, b, e, c, d, f });
    var det = (a * d) - (b * c);
    if (det == 0) {
        return null;
    }
    var ans = [2]f64{ 0, 0 };
    ans[0] = (d * e - b * f) / det;
    ans[1] = (-c * e + a * f) / det;
    return ans;
}

const Stone = struct {
    name: []const u8,
    pos: [3]i64,
    speed: [3]i64,

    pub fn init(name: []const u8) Stone {
        return Stone{ .name = name, .pos = [3]i64{ 0, 0, 0 }, .speed = [3]i64{ 0, 0, 0 } };
    }

    pub fn intersect(self: Stone, other: Stone, area: [2]f64) bool {
        var t_f = solve2x2(@floatFromInt(self.speed[0]), @floatFromInt(-other.speed[0]), @floatFromInt(self.speed[1]), @floatFromInt(-other.speed[1]), @floatFromInt(other.pos[0] - self.pos[0]), @floatFromInt(other.pos[1] - self.pos[1]));
        //std.debug.print("Stone {any} and {any} intersect on {any}\n", .{ self.speed, other.speed, t_f });
        if (t_f == null) {
            return false;
        }
        var t = t_f.?;
        if (t[0] >= 0 and t[1] >= 0) {
            var insideArea = true;
            var pos_intersect: [2]f64 = undefined;
            for (0..2) |ix| {
                pos_intersect[ix] = t[0] * @as(f64, @floatFromInt(self.speed[ix])) + @as(f64, @floatFromInt(self.pos[ix]));
                insideArea = insideArea and (pos_intersect[ix] >= area[0] and pos_intersect[ix] <= area[1]);
            }
            return insideArea;
        }
        return false;
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

fn solve(data: anytype, example: bool) !void {
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

    var search_area = if (example) [2]f64{ 7, 27 } else [2]f64{ 200000000000000, 400000000000000 };
    var part1: i32 = 0;
    for (stones.items, 1..) |stone, ix| {
        for (stones.items[ix..]) |other| {
            if (stone.intersect(other, search_area)) {
                part1 += 1;
            }
        }
    }
    std.debug.print("Part 1 = {} \n", .{part1});
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

    try solve(if (example) fileDataEx else fileData, example);
}
