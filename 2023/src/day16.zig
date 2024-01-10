const std = @import("std");
const ascii = @import("std").ascii;
const utils = @import("./utils.zig");

const fileData = @embedFile("./files/day16.txt");
const fileDataEx = @embedFile("./files/day16ex.txt");

const Allocator = std.mem.Allocator;

fn is_out_of_bounds(beam: [4]i32, shape: [2]i32) bool {
    if (beam[0] < 0 or beam[1] < 0 or beam[0] >= shape[0] or beam[1] >= shape[1]) {
        return true;
    }
    return false;
}

fn add_new_from_obstacle(beam: [4]i32, obstacle: u8, results: *std.ArrayList([4]i32)) !void {
    //std.debug.print("beam at {any} at {c}\n", .{ beam, obstacle });
    switch (obstacle) {
        '|' => if (@abs(beam[3]) == 1) {
            try results.append([4]i32{ beam[0], beam[1], 1, 0 });
            try results.append([4]i32{ beam[0], beam[1], -1, 0 });
            return;
        },
        '-' => if (@abs(beam[2]) == 1) {
            try results.append([4]i32{ beam[0], beam[1], 0, 1 });
            try results.append([4]i32{ beam[0], beam[1], 0, -1 });
            return;
        },
        '/' => {
            try results.append([4]i32{ beam[0], beam[1], -beam[3], -beam[2] });
            return;
        },
        '\\' => {
            try results.append([4]i32{ beam[0], beam[1], beam[3], beam[2] });
            return;
        },
        '.' => {},
        else => unreachable,
    }
    try results.append([4]i32{ beam[0], beam[1], beam[2], beam[3] });
}

fn get_activated_by_beam(map: [][]const u8, shape: [2]i32, init_beam: [4]i32, allocator: Allocator) !i32 {
    var queue = std.ArrayList([4]i32).init(allocator);

    var activated_beams = std.AutoHashMap([4]i32, u8).init(allocator);
    var activated_pos = std.AutoHashMap([2]i32, u8).init(allocator);
    try queue.append(init_beam);
    while (queue.items.len > 0) {
        var beam = queue.pop();

        // move beam
        beam[0] += beam[2];
        beam[1] += beam[3];

        if (is_out_of_bounds(beam, shape)) {
            continue;
        }

        //std.debug.print("Queue length = {}, beam at {any} at {c}\n", .{ queue.items.len, beam, map[@intCast(beam[0])][@intCast(beam[1])] });
        if (activated_beams.contains(beam)) {
            continue;
        }
        try activated_beams.put(beam, 0);
        try activated_pos.put([2]i32{ beam[0], beam[1] }, 0);
        try add_new_from_obstacle(beam, map[@intCast(beam[0])][@intCast(beam[1])], &queue);
    }
    return @intCast(activated_pos.count());
}

fn solve(data: anytype) !void {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();

    var len: usize = 0;
    var splitsLines = std.mem.split(u8, data, "\n");
    while (splitsLines.next()) |_| {
        len += 1;
    }
    var map: [][]const u8 = undefined;
    map = try allocator.alloc([]const u8, len);
    var splits = std.mem.split(u8, data, "\n");
    for (map, 0..) |_, i| {
        map[i] = splits.next() orelse unreachable;
    }
    // Find start position
    var maxX: usize = len;
    var maxY: usize = map[0].len;
    var shape = [2]i32{ @intCast(maxX), @intCast(maxY) };
    std.debug.print("Find beam map of {} x {} {any} \n", .{ maxX, maxY, shape });

    var solutions = std.ArrayList(i32).init(allocator);

    for (0..maxX) |i| {
        var ix: i32 = @intCast(i);
        try solutions.append(try get_activated_by_beam(map, shape, [4]i32{ ix, -1, 0, 1 }, allocator));
        try solutions.append(try get_activated_by_beam(map, shape, [4]i32{ ix, shape[1], 0, -1 }, allocator));

        try solutions.append(try get_activated_by_beam(map, shape, [4]i32{ -1, ix, 1, 0 }, allocator));
        try solutions.append(try get_activated_by_beam(map, shape, [4]i32{ shape[0], ix, -1, 0 }, allocator));
    }
    std.debug.print("Part 1 = {}\n", .{solutions.items[0]});
    std.sort.insertion(i32, solutions.items, comptime {}, comptime std.sort.desc(i32));
    std.debug.print("Part 2 = {}\n", .{solutions.items[0]});
}

pub fn main() !void {
    const argv = std.os.argv;
    var example: bool = false;
    std.log.info("Hello day 16: {s}", .{argv});
    for (argv) |args| {
        if (std.mem.eql(u8, args[0..2], "ex")) {
            example = true;
        }
    }

    try solve(if (example) fileDataEx else fileData);
}
