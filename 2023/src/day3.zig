const std = @import("std");
const ascii = @import("std").ascii;
const utils = @import("./utils.zig");

const Point2D = utils.Point2D;

const dataFile = @embedFile("./files/day3.txt");
const dataFileEx = @embedFile("./files/day3ex.txt");

const arrayType = std.ArrayListAligned([]const u8, null);
const arrayType2 = std.ArrayListAligned(i32, null);
const Allocator = std.mem.Allocator;

fn fill_matrix(array: *arrayType, data: anytype) !void {
    var splits = std.mem.split(u8, data, "\n");
    while (splits.next()) |line| {
        try array.append(line);
    }
}

fn findStarInNeighbourghs(map: *arrayType, pos: Point2D) ?Point2D {
    const directions = utils.getDirections();
    for (directions) |dir| {
        var newPos = pos.add(&dir);
        var x = newPos.getX(map.items.len) catch {
            continue;
        };
        var y = newPos.getY(map.items[0].len) catch {
            continue;
        };
        var item = map.items[x][y];
        if (item == '*') {
            return newPos;
        }
    }
    return null;
}

fn symbolInNeighbourghs(map: *arrayType, pos: Point2D) bool {
    const directions = utils.getDirections();
    for (directions) |dir| {
        var newPos = pos.add(&dir);
        var x = newPos.getX(map.items.len) catch {
            continue;
        };
        var y = newPos.getY(map.items[0].len) catch {
            continue;
        };
        var item = map.items[x][y];
        if (!ascii.isDigit(item) and item != '.') {
            return true;
        }
    }
    return false;
}

fn getNumber(array: *std.ArrayList(i32)) i32 {
    var res: i32 = 0;
    for (array.items, 0..) |num, ix| {
        res += num * std.math.pow(i32, 10, @intCast(array.items.len - ix - 1));
    }
    return res;
}

fn solve(map: *arrayType) !void {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();

    var tmp_number = std.ArrayList(i32).init(allocator);
    defer tmp_number.deinit();

    var sum: i32 = 0;
    var sum_part2: i32 = 0;
    var number_found: bool = false;
    var symbol_found: bool = false;
    var part2_pos: ?Point2D = null;
    var gear_hash = std.AutoHashMap(Point2D, i32).init(allocator);
    for (map.items, 0..) |line, il| {
        for (line, 0..) |item, ic| {
            var endOfNumber = !ascii.isDigit(item) or ic == line.len;
            if (ascii.isDigit(map.items[il][ic])) {
                try tmp_number.append(item - '0');
                number_found = true;
                std.log.debug("Partial number found = {any}, ", .{tmp_number.items});
                if (symbolInNeighbourghs(map, Point2D.new(il, ic))) {
                    symbol_found = true;
                    std.log.debug("Symbol found, ", .{});
                }
                var start_position = findStarInNeighbourghs(map, Point2D.new(il, ic));
                if (start_position != null) {
                    part2_pos = start_position;
                }
            }
            if (endOfNumber) {
                if (symbol_found) {
                    var num = getNumber(&tmp_number);
                    std.log.debug("Number found = {any} -> {}\n", .{ tmp_number.items, num });
                    sum += num;
                    if (part2_pos != null) {
                        if (gear_hash.contains(part2_pos.?)) {
                            var gear_ratio = gear_hash.get(part2_pos.?).? * num;
                            std.log.debug("Gear ratio = {}\n", .{gear_ratio});
                            sum_part2 += gear_ratio;
                        } else {
                            try gear_hash.put(part2_pos.?, num);
                        }
                    }
                }
                part2_pos = null;
                number_found = false;
                symbol_found = false;
                tmp_number.clearAndFree();
            }
        }
    }
    std.log.info("Part 1 result = {}", .{sum});
    std.log.info("Part 2 result = {}", .{sum_part2});
}

pub fn main() !void {
    const argv = std.os.argv;
    var debug: bool = false;
    var example: bool = false;
    std.log.info("Hello day 3: {s}", .{argv});
    for (argv) |args| {
        if (std.mem.eql(u8, args[0..5], "debug")) {
            debug = true;
        }
        if (std.mem.eql(u8, args[0..2], "ex")) {
            example = true;
        }
    }
    std.log.info("Args: debug = {}, example = {}", .{ debug, example });

    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();
    var map = std.ArrayList([]const u8).init(allocator);
    if (example) {
        try fill_matrix(&map, dataFileEx);
    } else {
        try fill_matrix(&map, dataFile);
    }
    for (map.items) |line| {
        std.log.debug("Output array : {s}\n", .{line});
    }

    try solve(&map);
}
