#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

int compute_index(int letters, int words, int sentences);

int main(void)
{
    string text = get_string("Place the text here: ");

    int letters = 0, words = 1, sentences = 0;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]))
        {
            letters++;
        }
        else if (text[i] == ' ')
        {
            words++;
        }
        else if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
    }

    int index = compute_index(letters, words, sentences);

    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

int compute_index(int letters, int words, int sentences)
{
    float L = ((float) letters / words) * 100;

    float S = ((float) sentences / words) * 100;

    float index = 0.0588 * L - 0.296 * S - 15.8;

    return round(index);
}
