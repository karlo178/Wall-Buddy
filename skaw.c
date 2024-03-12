#include <stdio.h>

// tu se ogarniasz czy dany rok jest rokiem przestępnym
int czyPrzestepny(int rok) {
    return (rok % 4 == 0 && rok % 100 != 0) || (rok % 400 == 0);
}

// patrzasz ile dni
int dniWMiesiacu(int miesiac, int rok) {
    int dniWMiesiacach[] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

    if (miesiac == 2 && czyPrzestepny(rok))
        return 29;
    else
        return dniWMiesiacach[miesiac];
}

// zaawansowana kurwa matematyka sprawdzasz tą różnice
int liczDni(int dzien1, int miesiac1, int rok1, int dzien2, int miesiac2, int rok2) {
    int dni = 0;

    while (dzien1 != dzien2 || miesiac1 != miesiac2 || rok1 != rok2) {
        dni++;

        //i pyk na kolejny dzien
        dzien1++;

        //końca miesiąca obczajasz
        if (dzien1 > dniWMiesiacu(miesiac1, rok1)) {
            dzien1 = 1;
            miesiac1++;

            //a tu koniec roku roku
            if (miesiac1 > 12) {
                miesiac1 = 1;
                rok1++;
            }
        }
    }

    return dni;
}

int main() {
    int dzien1, miesiac1, rok1;
    int dzien2, miesiac2, rok2;

    printf("Podaj pierwsza date (dzien miesiac rok): ");
    scanf("%d %d %d", &dzien1, &miesiac1, &rok1);

    printf("Podaj druga date (dzien miesiac rok): ");
    scanf("%d %d %d", &dzien2, &miesiac2, &rok2);

    int roznicaDni = liczDni(dzien1, miesiac1, rok1, dzien2, miesiac2, rok2);

    printf("Liczba dni pomiedzy podanymi datami: %d\n", roznicaDni);

    return 0;
}
