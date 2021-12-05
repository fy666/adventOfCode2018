package main

import (
	"bufio"
	"flag"
	"fmt"
	"log"
	"os"
	"strconv"
)

func sum(data []int) (res int) {
	for _, v := range data {
		res += v
	}
	return
}

func product(data []int) (res int) {
	res = 1
	for _, v := range data {
		res *= v
	}
	return
}

func min(data []int) (res int) {
	res = data[0]
	for _, v := range data {
		if v < res {
			res = v
		}
	}
	return
}

func max(data []int) (res int) {
	res = data[0]
	for _, v := range data {
		if v > res {
			res = v
		}
	}
	return
}

func getInt(val bool) int {
	if val {
		return 1
	}
	return 0
}

func getLitteral(hex string) (int, string) {
	ix := 0
	tmp := ""
	for hex[ix] == '1' {
		tmp += hex[ix+1 : ix+5]
		ix = ix + 5
	}
	tmp += hex[ix+1 : ix+5]
	ix = ix + 5
	litteralValue, _ := strconv.ParseUint(tmp, 2, 64)
	return int(litteralValue), hex[ix:]

}

func doOperation(data []int, code uint64) int {

	switch code {
	case 0:
		return sum(data)
	case 1:
		return product(data)
	case 2:
		return min(data)
	case 3:
		return max(data)
	case 5:
		return getInt(data[0] > data[1])
	case 6:
		return getInt(data[0] < data[1])
	case 7:
		return getInt(data[0] == data[1])
	default:
	}
	return 0
}

func getPacketValue(hex string) (uint64, int, string) {
	ix := 0
	if len(hex) > 7 {
		version, _ := strconv.ParseUint(hex[ix:ix+3], 2, 64)
		id, _ := strconv.ParseUint(hex[ix+3:ix+6], 2, 64)
		ix = ix + 6
		if id == 4 {
			value, new_hex := getLitteral(hex[ix:])
			return version, value, new_hex
		} else {
			values := make([]int, 0, 50)
			if hex[ix] == '1' {
				nSubs, _ := strconv.ParseUint(hex[ix+1:ix+12], 2, 64)
				ix = ix + 12
				hex = hex[ix:]
				for num_sub := 0; num_sub < int(nSubs); num_sub++ {
					v, value, new_hex := getPacketValue(hex)
					hex = new_hex
					version += v
					values = append(values, value)
				}
			} else {
				dataSize, _ := strconv.ParseUint(hex[ix+1:ix+16], 2, 64)
				ix = ix + 16
				hex = hex[ix:]
				consumed_data := 0
				//fmt.Println("Operator with size", dataSize)
				for consumed_data < int(dataSize) {
					v, value, new_hex := getPacketValue(hex)
					consumed_data += len(hex) - len(new_hex)
					hex = new_hex
					version += v
					values = append(values, value)
				}
			}
			result := doOperation(values, id)
			return version, result, hex
		}
	}
	fmt.Println("Something's wrong")
	return 0, 0, hex
}

func main() {
	var test = flag.Bool("test", false, "Use test input")
	flag.Parse()
	fileName := "day16.txt"
	if *test {
		fileName = "day16_test.txt"
	}
	file, err := os.Open(fileName)
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()
	scanner := bufio.NewScanner(file)
	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}

	for scanner.Scan() {
		hex_input := scanner.Text()
		output := ""
		for ix := 0; ix < len(hex_input); ix++ {
			decimal, _ := strconv.ParseUint(string(hex_input[ix]), 16, 64)
			tmp := strconv.FormatInt(int64(decimal), 2)
			to_add := 4 - len(tmp)
			for z := 0; z < to_add; z++ {
				tmp = "0" + tmp
			}
			output = output + tmp
		}
		version, value, _ := getPacketValue(output)
		fmt.Println("Version =", version, "value =", value)
	}
}
