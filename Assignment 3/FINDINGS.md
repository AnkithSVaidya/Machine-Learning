# Telco Monthly Charge Model — Findings Summary

Multivariable linear regression predicting `target` (car price) from the fourteen indicators, trained on an 80/20 split (`random_state=42`)
`car details v4.csv`. Full code in `assignment_3.ipynb`.

## 1. Most significant numerical contribution
| Service | Value |
|---|---|
| Year | +13 %/year |
| Seating Capacity | -7.1 %/seat |
| Fuel Tank Capacity | +0.54 %/L |
| Width | +0.058 %/m |
| Length | +0.048 %/m |
| Engine | +0.039 %/cc |
| Height | +0.017 %/m |
| Kilometer | +0.017 %/km |

The main surprise here is seating capacity. The reason for the negative relationship with seating capacity is because the lenght, width, and height are already accounted for. This means that at the same length, width, and height a lower seating capacity is higher price, which likely means more luxury.

## 2. Most significant Makes
| Make | % Increase |
|---|---|
| Porsche | +132.7% |
| Land Rover | +100.6% |
| MINI | +44.52% |
| BMW | +39.39% |
| Mercedes-Benz | +39.13% |
| Volvo | +31.67% |
| Tata | -29.29% |
| Jaguar | +27.37% |
| Renault | -24.43% |
| Mahindra | -23.24% |

As can be seen, the Porche is the most valuable make, increasing the car's value by 133%.
