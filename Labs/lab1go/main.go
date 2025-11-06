package main

import (
	"fmt"
	"math"
)

func inputCoefficients() (float64, float64, float64, error) {
	var a, b, c float64
	fmt.Println("Введите коэффициенты A B C:")
	_, err := fmt.Scanf("%f %f %f", &a, &b, &c)
	if err != nil {
		return 0, 0, 0, err
	}
	return a, b, c, nil
}

func getRoots(a, b, c float64) []float64 {
	discriminant := b*b - 4*a*c
	sqrtD := math.Sqrt(discriminant)
	var roots []float64
	roots = append(roots, ((-b + sqrtD) / (2 * a)))
	roots = append(roots, (-b-sqrtD)/(2*a))
	return roots
}

func main() {
	a, b, c, err := inputCoefficients()
	var roots []float64
	if err != nil {
		fmt.Println("Ошибка ввода:", err)
		return
	}
	if a == 0 {
		fmt.Println("А не может быть равным нулю")
		return
	}
	discriminant := b*b - 4*a*c
	if discriminant < 0 {
		fmt.Println("Корней нет (дискриминант < 0)")
		return
	}

	for _, y := range getRoots(a, b, c) {
		if y == 0 {
			roots = append(roots, 0)
		}
		if y > 0 {
			roots = append(roots, math.Sqrt(y), -math.Sqrt(y))
		}
	}

	if len(roots) == 0 {
		fmt.Println("Корней нет (отрицательные корни уравнения по x^2)")
		return
	}
	fmt.Println("Корни уравнения:")
	for _, root := range roots {
		fmt.Printf("%.6f\n", root)
	}
}
