const std = @import("std");
const ascii = @import("std").ascii;

const fileData = @embedFile("./files/day2.txt");
const fileDataEx = @embedFile("./files/day2ex.txt");
//const cregex = @import("ctregex");
const Regex = @import("zig-regex").Regex;

const cubes = struct { r: i32, g: i32, b: i32 };

fn get_match(line: []const u8, color: []const u8) !i32 {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();
    var re = try Regex.compile(allocator, color);

    var captures = try re.captures(line);
    var result: i32 = 0;
    if (captures != null) {
        var cap = captures.?.sliceAt(1);
        result = try std.fmt.parseInt(i32, cap.?, 10);
    }
    return result;
}

fn get_full_match(line: []const u8) !cubes {
    var result: cubes = undefined;
    result.r = try get_match(line, "(\\d+) red");
    result.b = try get_match(line, "(\\d+) blue");
    result.g = try get_match(line, "(\\d+) green");
    return result;
}

fn solve(data: anytype, rule: cubes) !void {
    var sum_part1: i32 = 0;
    var sum_part2: i32 = 0;

    var splits = std.mem.split(u8, data, "\n");
    var game: i32 = 1;
    while (splits.next()) |line| {
        var subsplit = std.mem.split(u8, line, ";");
        var valid_game: bool = true;
        var maxs = cubes{ .r = 0, .g = 0, .b = 0 };

        // Treat one game
        while (subsplit.next()) |item| {
            var res = try get_full_match(item);
            if (res.r > rule.r or res.g > rule.g or res.b > rule.b) {
                valid_game = false;
            }
            maxs.r = @max(res.r, maxs.r);
            maxs.g = @max(res.g, maxs.g);
            maxs.b = @max(res.b, maxs.b);
        }

        if (valid_game) {
            //std.debug.print("{s} -> Valid game {}\n", .{ line, game });
            sum_part1 += game;
        }
        //std.debug.print("Game {} ->  {any} = {}\n", .{ game, maxs, (maxs.r * maxs.g * maxs.b) });
        sum_part2 += (maxs.r * maxs.g * maxs.b);
        game += 1;
    }

    std.debug.print("Part 1 = {}, Part 2 = {}\n", .{ sum_part1, sum_part2 });
}

pub fn main() !void {
    const argv = std.os.argv;
    var example: bool = false;
    std.log.info("Hello day 3: {s}", .{argv});
    for (argv) |args| {
        if (std.mem.eql(u8, args[0..2], "ex")) {
            example = true;
        }
    }

    std.debug.print("Hello day 2!\n", .{});
    if (example) {
        try solve(fileDataEx, cubes{ .r = 12, .g = 13, .b = 14 });
    } else {
        try solve(fileData, cubes{ .r = 12, .g = 13, .b = 14 });
    }
}
