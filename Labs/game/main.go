package main

import (
	"bufio"
	"fmt"
	"os"
	"strings"
)

type room struct {
	name    string
	paths   []*room
	content []*storage
	locked  bool
}

type storage struct {
	name  string
	items []*item
}

func (s *storage) removeItemFromStorage(item *item) {
	for i, it := range s.items {
		if it == item {
			s.items = append(s.items[:i], s.items[i+1:]...)
			return
		}
	}
}

type item struct {
	name string
}

type player struct {
	currentRoom *room
	inv         []*item
	equipped    *item
}

func (p *player) moveTo(r string) string {

	for _, path := range p.currentRoom.paths {
		if path.name == r {
			if path.locked {

				return "дверь закрыта"
			}
			p.currentRoom = path
			//fmt.Println("успех, перешёл в", path.name)
			switch path {
			case corridor:
				return "ничего интересного. можно пройти - кухня, комната, улица"
			case livingRoom:
				return "ты в своей комнате. можно пройти - коридор"
			case kitchen:
				return "кухня, ничего интересного. можно пройти - коридор"
			case street:
				return "на улице весна. можно пройти - домой"
			}

		}
	}
	//fmt.Println("Cannot move to", r)
	return "нет пути в " + r
}

func (p *player) takeItem(itemName string) string {

	for _, storage := range p.currentRoom.content {
		for _, item := range storage.items {

			if p.equipped == nil {
				//fmt.Println("некуда класть")
				return "некуда класть"

			}

			if item.name == itemName {
				p.inv = append(p.inv, item)
				storage.removeItemFromStorage(item)
				//fmt.Println("Вы взяли:", item.name)
				return "предмет добавлен в инвентарь: " + itemName
			}
		}
	}
	//fmt.Println("Item not found:", itemName)
	return "нет такого"
}

func (p *player) removeItem(itemName string) {
	for i, item := range p.inv {
		if item.name == itemName {
			p.inv = append(p.inv[:i], p.inv[i+1:]...)
			return
		}
	}
}

func (p *player) equipItem(itemName string) string {
	for _, storage := range p.currentRoom.content {
		for _, item := range storage.items {
			if item.name == itemName {
				p.equipped = item
				storage.removeItemFromStorage(item)
				//fmt.Println("Вы надели:", item.name)
				return "вы надели: " + item.name
			}
		}
	}
	//fmt.Println("Item not found:", itemName)
	return "нет такого"
}

func (p *player) inspectRoom() string {
	var location, goals string
	var items, possiblePaths []string
	switch p.currentRoom.name {
	case "улица":
		location = "ты находишься на улице"
	case "кухня":
		location = "ты находишься на кухне"
	case "коридор":
		location = "ты находишься в коридоре"
	case "комната":
		for _, storage := range p.currentRoom.content {
			if len(storage.items) != 0 {
				location = ""
				break
			}
			location = "пустая комната"
		}
	}
	//items = append(items, "")
	for _, storage := range p.currentRoom.content {
		//fmt.Println("In storage:", storage.name)
		if storage.name == "стол" && len(storage.items) != 0 {
			var itemsTable []string
			//items = append(items, ", на столе:")
			for _, item := range storage.items {
				//fmt.Println(" - Item:", item.name)
				itemsTable = append(itemsTable, item.name)
			}
			table := ("на столе: " + strings.Join(itemsTable, ", "))
			items = append(items, table)
		}

		if storage.name == "стул" && len(storage.items) != 0 {
			var itemsChair []string
			//items = append(items, ", на столе:")
			for _, item := range storage.items {
				//fmt.Println(" - Item:", item.name)
				itemsChair = append(itemsChair, item.name)
			}
			chair := ("на стуле: " + strings.Join(itemsChair, ", "))
			items = append(items, chair)
		}

	}
	for _, path := range p.currentRoom.paths {
		possiblePaths = append(possiblePaths, path.name)
	}
	if len(items) != 0 && len(location) != 0 {
		location = location + ", "
	}

	if p.currentRoom == kitchen {
		goals = ", надо идти в универ"

		if p.equipped == nil {
			goals = ", надо собрать рюкзак и идти в универ"
		}
	}
	if p.currentRoom == street {
		return (location + strings.Join(items, ", ") + goals + ". можно пройти - " + "домой")
	}
	return (location + strings.Join(items, ", ") + goals + ". можно пройти - " + strings.Join(possiblePaths, ", "))

}

func (p *player) useItem(items []string) string {
	if len(items) > 2 {
		return "слишком много аргументов"
	}
	for _, item := range p.inv {
		if item.name == items[0] {
			if len(items) > 1 && items[1] == "дверь" && item.name == "ключи" && p.currentRoom == corridor {
				street.locked = false
				return "дверь открыта"
			}
			if item.name == "чай" {
				p.removeItem("чай")
				return "вы выпили чай. вкусно и бодрит!"

			}
			if item.name == "конспекты" {
				return "вы прочитали конспекты. теперь вы знаете все!"

			}

			return "не к чему применить"
		}
	}

	return "нет предмета в инвентаре - " + items[0]
}

/* func (p *player) inspectInventory() string {
	fmt.Println("Inventory:")
	for _, item := range p.inv {
		fmt.Println(" - Item:", item.name)
	}
	return "success"
} */

var corridor, livingRoom, kitchen, street *room
var p *player

func initGame() {

	corridor = &room{
		name:    "коридор",
		content: []*storage{{name: "шкаф", items: []*item{}}},
		locked:  false,
	}
	livingRoom = &room{
		name: "комната",
		content: []*storage{
			{name: "стол", items: []*item{{name: "ключи"}, {name: "конспекты"}}},
			{name: "стул", items: []*item{{name: "рюкзак"}}},
		},
		locked: false,
	}
	kitchen = &room{
		name: "кухня",
		content: []*storage{
			{name: "стол", items: []*item{{name: "чай"}}},
		},
		locked: false,
	}
	street = &room{
		name:    "улица",
		content: []*storage{},
		locked:  true,
	}
	p = &player{
		currentRoom: kitchen,
		inv:         []*item{},
		equipped:    nil,
	}

	corridor.paths = []*room{livingRoom, kitchen, street}
	livingRoom.paths = []*room{corridor}
	kitchen.paths = []*room{corridor}
	street.paths = []*room{corridor}

}

func handleCommand(command string) string {

	parsedCommand := strings.Split(command, " ")
	if len(parsedCommand) > 3 {
		return "слишком много аргументов"
	}
	switch parsedCommand[0] {
	case "идти":
		if parsedCommand[1] == "домой" && p.currentRoom == street {
			return (p.moveTo("коридор"))
		}
		return (p.moveTo(parsedCommand[1]))
	case "осмотреться":
		return (p.inspectRoom())
	case "взять":
		return (p.takeItem(parsedCommand[1]))
	case "надеть":
		return (p.equipItem(parsedCommand[1]))
	case "применить":
		return (p.useItem(parsedCommand[1:]))
	default:
		return "неизвестная команда"
	}

}

func main() {
	initGame()
	fmt.Println("Доступные команды: \"осмотреться\", \"идти (куда)\", \"применить (что, куда)\", \"надеть (что)\", \"взять (что)\"")
	fmt.Println(p.inspectRoom())
	sc := bufio.NewScanner(os.Stdin)
	for {
		sc.Scan()
		fmt.Println(handleCommand(sc.Text()))
	}
}
