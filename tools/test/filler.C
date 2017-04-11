/** To fill ROOT histograms from python **/

#include "TH1.h"
#include "TH2.h"
#include "TProfile.h"
#include "TProfile2D.h"

// TH1; TH2 and TProfile without weights
void fill(TH1* h, int N, Double_t *x, Double_t *y = 0)
{
  for (int i = 0; i < N; ++i)
    h->Fill(x[i], (y ? y[i] : 1.) );
}

// TProfile with weights
void fill(TProfile* h, int N, Double_t *x, Double_t *y, Double_t *w)
{
  for (int i = 0; i < N; ++i)
    h->Fill(x[i], y[i], w[i] );
}


// TH2, TProfile2D without weights
void fill(TH2* h, int N, Double_t *x, Double_t *y, Double_t *z = 0)
{
  for (int i = 0; i < N; ++i)
    h->Fill(x[i], y[i], (z ? z[i] : 1.) );
}

// TProfile2D with weights
void fill(TProfile2D* h, int N, Double_t *x, Double_t *y, Double_t *z, Double_t *w)
{
  for (int i = 0; i < N; ++i)
    h->Fill(x[i], y[i], z[i], w[i]);
}

// TH3
void fill(TH3* h, int N, Double_t *x, Double_t *y, Double_t *z, Double_t *w = 0)
{
  for (int i = 0; i < N; ++i)
    h->Fill(x[i], y[i], z[i], (w ? w[i]: 1.) );
}
