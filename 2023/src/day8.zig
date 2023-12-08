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
    var re = try Regex.compile(allocator, "([A-Z]+) = \\(([A-Z]+), ([A-Z]+)\\)");

    var captures = try re.captures(line);
    if (captures != null) {
        //AAA = (BBB, CCC)
        var map = Map{ .left = undefined, .right = undefined };
        std.mem.copy(u8, &map.left, captures.?.sliceAt(2).?);
        std.mem.copy(u8, &map.right, captures.?.sliceAt(3).?);
        var tmp: [3]u8 = undefined;
        std.mem.copy(u8, &tmp, captures.?.sliceAt(1).?);
        //std.debug.print("map L={s}, R={s}\n", .{ map.left, map.right });
        try hashmap.put(tmp, map);
    } else {
        std.debug.print("{s} map not found\n", .{line});
        unreachable;
    }
}

pub const Map = struct {
    left: [3]u8,
    right: [3]u8,
};

fn enchCheckP1(pos: [3]u8) bool {
    return std.mem.eql(u8, &pos, "ZZZ");
}

fn enchCheckP2(pos: [3]u8) bool {
    return pos[2] == 'Z';
}

fn solveMap(network: *std.AutoHashMap([3]u8, Map), commands: []const u8, start: [3]u8, comptime endCheck: fn (pos: [3]u8) bool) i32 {
    var steps: i32 = 1;
    var step_vec: usize = 0;
    var position = start;
    while (true) : (steps += 1) {
        var pos_map = network.get(position).?;
        switch (commands[step_vec]) {
            'R' => position = pos_map.right,
            'L' => position = pos_map.left,
            else => unreachable,
        }
        step_vec = (step_vec + 1) % commands.len; //
        //std.debug.print("Going to {s}\n", .{position});
        if (endCheck(position)) {
            break;
        }
    }
    return steps;
}

fn gcd(a: i64, b: i64) i64 {
    if (b == 0)
        return a;
    return gcd(b, @rem(a, b));
}

fn lcm(a: i64, b: i64) i64 {
    if (a > b) {
        return @divExact(a, gcd(a, b)) * b;
    } else {
        return @divExact(b, gcd(a, b)) * a;
    }
}

fn solve(data: anytype) !void {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();
    var network = std.AutoHashMap([3]u8, Map).init(allocator);
    var commands: []const u8 = undefined;
    var splits = std.mem.split(u8, data, "\n\n");
    var ix: i32 = 0;
    while (splits.next()) |line| : (ix += 1) {
        if (ix == 0) {
            commands = line;
            continue;
        }
        var map_lines = std.mem.split(u8, line, "\n");
        while (map_lines.next()) |l| {
            try fill_hashmap(l, &network);
        }
    }

    std.debug.print("Network map size = {}\n", .{network.count()});

    var it = network.iterator();
    while (it.next()) |item| {
        std.debug.print("{s} -> ({s}, {s})\n", .{ item.key_ptr.*[0..], item.value_ptr.*.right[0..], item.value_ptr.*.left[0..] });
    }

    // Part 1
    var steps: i32 = 1;
    var step_vec: usize = 0;
    var position = [_]u8{ 'A', 'A', 'A' };
    while (true) : (steps += 1) {
        var pos_map = network.get(position).?;
        switch (commands[step_vec]) {
            'R' => position = pos_map.right,
            'L' => position = pos_map.left,
            else => unreachable,
        }
        step_vec = (step_vec + 1) % commands.len; //
        // std.debug.print("Going to {s}\n", .{position});
        if (std.mem.eql(u8, &position, "ZZZ")) {
            break;
        }
    }

    var part1 = solveMap(&network, commands, [3]u8{ 'A', 'A', 'A' }, enchCheckP1);
    std.debug.print("Part 1 steps = {}\n", .{part1});
    var ik = network.keyIterator();

    var lcm_var: i64 = part1;
    while (ik.next()) |key| {
        if (key[2] == 'A') {
            //std.debug.print("{s}\n", .{key});
            var tmpSolve = solveMap(&network, commands, key.*, enchCheckP2);

            lcm_var = lcm(lcm_var, tmpSolve);
            std.debug.print("Part 2 {s} steps = {}, lcm = {}\n", .{ key, tmpSolve, lcm_var });
        }
    }
    std.debug.print("Part 2 steps = {}\n", .{lcm_var});
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
