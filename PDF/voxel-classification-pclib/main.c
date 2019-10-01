void
cvoxelstats(double *mean, double *stdr, unsigned int *count,
           const double *v, const unsigned int *x,
           const unsigned int n, const unsigned int m) {
    // grid cell mean and std by welford
    unsigned int i, k;
    double *dd, du, dv;

    // squared distances from the mean
    dd = malloc(m * sizeof(double));
    if(!dd)
        exit(EXIT_FAILURE);

    // assign points to grid cells k
    for(i = 0; i < n; i++) {
        k = x[i];
        dv = v[i] - mean[k];
        count[k]++;
        mean[k] += dv / count[k];
        du = v[i] - mean[k];
        dd[k] += du * dv;
    }

    for(i = 0; i < m; i++) {
        if(count[i] > 1)
            stdr[i] = sqrt(dd[i]/(count[i]-1));
        else
            stdr[i] = sqrt(dd[i]/count[i]);
    }
    free(dd);
}

void
cvoxelize(unsigned int *r, const unsigned int *x,
         const unsigned int n, const unsigned int m) {
    unsigned int i, j, l;
    unsigned int *a[m];

    // alloc jagged array a
    for(i = 0; i < m; i++) {
        a[i] = malloc(8 * sizeof(unsigned int));
        if(!a[i])
            exit(EXIT_FAILURE);
        a[i][0] = 8;
        a[i][1] = 2;
    }

    // assign points to grid cells
    for(i = 0; i < n; i++) {
        j = x[i];
        a[j][a[j][1]++] = i;
        if(a[j][0] == a[j][1]) {
            a[j][0] *= 2;
            a[j] = realloc(a[j], a[j][0] * sizeof(unsigned int));
            if(!a[j])
                exit(EXIT_FAILURE);
        }
    }

    l = m + 1;
    for(i = 0; i < m; i++) {
        r[i] = l;
        for(j = 2; j < a[i][1]; j++)
            r[l++] = a[i][j];
        free(a[i]);
    }
    r[m] = l;
}

