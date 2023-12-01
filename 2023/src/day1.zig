const std = @import("std");
const ascii = @import("std").ascii;

const data = @embedFile("./files/day1.txt");

pub fn read_and_count_all(part2: bool) !void {
    var arena_state = std.heap.ArenaAllocator.init(std.heap.c_allocator);
    defer arena_state.deinit();
    const allocator = arena_state.allocator();

    var sum: i32 = 0;
    var splits = std.mem.split(u8, data, "\n");

    const numbers = [_][:0]const u8{ "zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine" };

    while (splits.next()) |line| {
        var calibration_values = std.ArrayList(i32).init(allocator);
        defer calibration_values.deinit();
        for (line, 0..) |letter, index| {
            for (numbers, 0..) |number, numberValue| {
                if (part2 and number.len + index <= line.len) {
                    if (std.mem.eql(u8, number, line[index .. index + number.len])) {
                        try calibration_values.append(@intCast(numberValue));
                    }
                }
            }
            if (ascii.isDigit(letter)) {
                try calibration_values.append((letter - '0'));
            }
        }
        if (calibration_values.items.len > 0) {
            sum += calibration_values.items[0] * 10;
            sum += calibration_values.items[calibration_values.items.len - 1];
        }
    }

    std.debug.print("{s}: Sum of calibration values = {}\n", .{ if (part2) "Part 2" else "Part 1", sum });
}

pub fn main() !void {
    std.debug.print("Hello day 1!\n", .{});
    try read_and_count_all(false);
    try read_and_count_all(true);
}
