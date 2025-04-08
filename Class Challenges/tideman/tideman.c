#include <cs50.h>
#include <stdio.h>
#include <string.h>

#define MAX 9

int preferences[MAX][MAX];
bool locked[MAX][MAX];

typedef struct
{
    int winner;
    int loser;
}
pair;

string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);

int main(int argc, string argv[])
{
    if (argc < 2)
    {
        printf("Uso: tideman [candidato ...]\n");
        return 1;
    }

    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Máximo de %i candidatos permitidos\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i] = argv[i + 1];
    }

    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            preferences[i][j] = 0;
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Número de eleitores: ");

    // Itera por cada voto
    for (int i = 0; i < voter_count; i++)
    {
        int ranks[candidate_count];

        // Pergunta o voto de cada eleitor
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Voto %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Voto inválido.\n");
                return 3;
            }
        }

        record_preferences(ranks);
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

bool vote(int rank, string name, int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i]) == 0)
        {
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

void record_preferences(int ranks[])
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = i + 1; j < candidate_count; j++)
        {
            preferences[ranks[i]][ranks[j]]++;
        }
    }
}

void add_pairs(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (preferences[i][j] > preferences[j][i])
            {
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                pair_count++;
            }
        }
    }
}

void sort_pairs(void)
{
    for (int i = 0; i < pair_count - 1; i++)
    {
        for (int j = i + 1; j < pair_count; j++)
        {
            int strength_i = preferences[pairs[i].winner][pairs[i].loser];
            int strength_j = preferences[pairs[j].winner][pairs[j].loser];
            if (strength_j > strength_i)
            {
                pair temp = pairs[i];
                pairs[i] = pairs[j];
                pairs[j] = temp;
            }
        }
    }
}

bool cycle(int winner, int loser)
{
    if (loser == winner)
    {
        return true;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        if (locked[loser][i])
        {
            if (cycle(winner, i))
            {
                return true;
            }
        }
    }
    return false;
}

void lock_pairs(void)
{
    for (int i = 0; i < pair_count; i++)
    {
        if (!cycle(pairs[i].winner, pairs[i].loser))
        {
            locked[pairs[i].winner][pairs[i].loser] = true;
        }
    }
}

void print_winner(void)
{
    for (int i = 0; i < candidate_count; i++)
    {
        bool is_winner = true;
        for (int j = 0; j < candidate_count; j++)
        {
            if (locked[j][i])
            {
                is_winner = false;
                break;
            }
        }
        if (is_winner)
        {
            printf("%s\n", candidates[i]);
            return;
        }
    }
}
