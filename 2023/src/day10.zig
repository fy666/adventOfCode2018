const std = @import("std");
const ascii = @import("std").ascii;
const utils = @import("./utils.zig");

const Point2D = utils.Point2D;

const fileData = @embedFile("./files/day10.txt");
const fileDataEx = @embedFile("./files/day10ex.txt");
const Regex = @import("zig-regex").Regex;

fn findStart(map: [][]const u8) Point2D {
    std.debug.print("Map = {c}\n", .{map[0][2]});
    for (map, 0..) |item, x| {
        for (item, 0..) |c, y| {
            if (c == 'S') {
                return Point2D.new(x, y);
            }
        }
        //std.debug.print("{s}\n", .{item});
    }
    unreachable;
}

fn get_pipe_outputs(pipe_pos: Point2D, pipe: u8) [2]Point2D {
    var res = switch (pipe) {
        '|' => [2]Point2D{ Point2D.new(pipe_pos.x - 1, pipe_pos.y), Point2D.new(pipe_pos.x + 1, pipe_pos.y) },
        '-' => [2]Point2D{ Point2D.new(pipe_pos.x, pipe_pos.y - 1), Point2D.new(pipe_pos.x, pipe_pos.y + 1) },
        'L' => [2]Point2D{ Point2D.new(pipe_pos.x - 1, pipe_pos.y), Point2D.new(pipe_pos.x, pipe_pos.y + 1) },
        'J' => [2]Point2D{ Point2D.new(pipe_pos.x - 1, pipe_pos.y), Point2D.new(pipe_pos.x, pipe_pos.y - 1) },
        '7' => [2]Point2D{ Point2D.new(pipe_pos.x + 1, pipe_pos.y), Point2D.new(pipe_pos.x, pipe_pos.y - 1) },
        'F' => [2]Point2D{ Point2D.new(pipe_pos.x + 1, pipe_pos.y), Point2D.new(pipe_pos.x, pipe_pos.y + 1) },
        else => unreachable,
    };
    return res;
}

fn solve(data: anytype) !void {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();
    var len: usize = 1;
    for (data) |c| {
        if (c == '\n') {
            len += 1;
        }
    }

    var map: [][]const u8 = undefined;
    var map2: [][]u8 = undefined;
    map = try allocator.alloc([]const u8, len);
    map2 = try allocator.alloc([]u8, len);
    std.debug.print("Type = {s}, len = {}\n", .{ @typeName(@TypeOf(map)), map.len });
    var splits = std.mem.split(u8, data, "\n");
    for (map, 0..) |_, i| {
        map[i] = splits.next() orelse unreachable;
        map2[i] = try allocator.alloc(u8, map[i].len);
        for (map2[i], 0..) |_, ic| {
            map2[i][ic] = 'X';
        }
        if (i == 0) {
            std.debug.print("Column length = {}\n", .{map[i].len});
        }
    }
    // Find start position
    var start_position = findStart(map);
    std.debug.print("Start pos = {}\n", .{start_position});

    var positions = std.ArrayList(Point2D).init(allocator);
    try positions.append(start_position);

    // Find first move
    var position = start_position;
    for (utils.get4Directions()) |dir| {
        position = start_position.add(&dir);
        var x = position.getX(len) catch {
            continue;
        };
        var y = position.getY(len) catch {
            continue;
        };
        if (map[x][y] != '.') {
            var possible_outputs = get_pipe_outputs(position, map[x][y]);
            if (utils.customEquality(possible_outputs[0], start_position) or utils.customEquality(possible_outputs[1], start_position)) {
                std.debug.print("Found first pos = {c} at {}\n", .{ map[x][y], position });
                break;
            }
        }
    }

    while (!utils.customEquality(position, start_position)) {
        var previous_position = positions.items[positions.items.len - 1];
        try positions.append(position);
        var x = try position.getX(len);
        var y = try position.getY(len);
        var current_pipe = map[x][y];
        //std.debug.print("Going to {c} ({})\n", .{ map[x][y], position });
        var possible_outputs = get_pipe_outputs(position, map[try position.getX(len)][try position.getY(len)]);
        if (utils.customEquality(possible_outputs[0], previous_position)) {
            position = possible_outputs[1];
        } else {
            position = possible_outputs[0];
        }

        if (current_pipe == '|' or current_pipe == '7' or current_pipe == 'F') {
            if (position.x > previous_position.x) {
                map2[x][y] = 'A';
            } else {
                map2[x][y] = 'D';
            }
        } else {
            map2[x][y] = 'P';
        }
    }
    std.debug.print("Part 1 loop = {}, max d = {}\n", .{ positions.items.len, positions.items.len / 2 });

    // What was pipe value for start ?
    var before = positions.items[positions.items.len - 1];
    var after = positions.items[1];
    var start_x = try start_position.getX(len);
    var start_y = try start_position.getY(len);
    var char_to_replace: u8 = ' ';
    if (start_position.x > after.x) {
        char_to_replace = 'A';
    } else {
        char_to_replace = 'D';
    }
    map2[start_x][start_y] = 'P';
    for ("|7F") |c| {
        var res = get_pipe_outputs(start_position, c);
        if ((utils.customEquality(res[0], before) and utils.customEquality(res[1], after)) or (utils.customEquality(res[1], before) and utils.customEquality(res[0], after))) {
            map2[start_x][start_y] = char_to_replace;
        }
    }

    // for (map2) |line| {
    //     std.debug.print("{s}\n", .{line});
    // }

    var part2_counter: i32 = 0;
    for (map2) |line| {
        var count_asc: i32 = 0;
        for (line) |c| {
            if (c == 'A') {
                count_asc += 1;
            } else if (c == 'D') {
                count_asc -= 1;
            } else if (c == 'X') {
                if (@mod(count_asc, 2) == 1) {
                    part2_counter += 1;
                }
            }
        }
    }

    std.debug.print("Part 2  {}\n", .{part2_counter});
}

pub fn main() !void {
    const argv = std.os.argv;
    var example: bool = false;
    std.log.info("Hello day 10: {s}", .{argv});
    for (argv) |args| {
        if (std.mem.eql(u8, args[0..2], "ex")) {
            example = true;
        }
    }
    try solve(if (example) fileDataEx else fileData);
}
