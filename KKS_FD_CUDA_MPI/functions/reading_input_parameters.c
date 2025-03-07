#include "inputReader.h"

void readInput_MPI(domainInfo *simDomain, controls *simControls,
                   simParameters *simParams, int rank, char *argv[])
{
    FILE *fr, *fp;
    if (fr = fopen(argv[1], "rt"))
    {
        if (!(rank))
            printf("\nReading input parameters from %s\n", argv[1]);
    }
    else
    {
        if (!(rank))
            printf("\nFile %s not found\n", argv[1]);
    }

    char tempbuff[1000];
    char outfile[100];
    char tmpstr1[100];
    char tmpstr2[100];

    sprintf(outfile, "DATA/Input.out");
    fp = fopen(outfile, "w");

    // Setting defaults
    simParams->alpha = 2.94;
    simParams->ISOTHERMAL = 1;
    simControls->multiphase = 1;
    simControls->restart = 0;
    simControls->writeHDF5 = 0;
    simControls->FUNCTION_ANISOTROPY = 0;
    simControls->ANISOTROPY = 0;
    simControls->ANISOTROPY_GRADIENT = 0;

    while (fgets(tempbuff,1000,fr))
    {
        sscanf(tempbuff,"%100s = %100[^;];", tmpstr1, tmpstr2);
        if (tmpstr1[0] != '#')
        {
            if (strcmp(tmpstr1, "MESH_X") == 0)
            {
                simDomain->MESH_X = atol(tmpstr2);
                fprintf(fp, "%s = %ld\n", tmpstr1, simDomain->MESH_X);
            }
            else if (strcmp(tmpstr1, "MESH_Y") == 0)
            {
                simDomain->MESH_Y = atol(tmpstr2);
                fprintf(fp, "%s = %ld\n", tmpstr1, simDomain->MESH_Y);

            }
            else if (strcmp(tmpstr1, "MESH_Z") == 0)
            {
                simDomain->MESH_Z = atol(tmpstr2);
                fprintf(fp, "%s = %ld\n", tmpstr1, simDomain->MESH_Z);
            }
            else if (strcmp(tmpstr1, "DELTA_X") == 0)
            {
                simDomain->DELTA_X = atof(tmpstr2);
                fprintf(fp, "%s = %le\n", tmpstr1, simDomain->DELTA_X);
            }
            else if (strcmp(tmpstr1, "DELTA_Y") == 0)
            {
                simDomain->DELTA_Y = atof(tmpstr2);
                fprintf(fp, "%s = %le\n", tmpstr1, simDomain->DELTA_Y);
            }
            else if (strcmp(tmpstr1, "DELTA_Z") == 0)
            {
                simDomain->DELTA_Z = atof(tmpstr2);
                fprintf(fp, "%s = %le\n", tmpstr1, simDomain->DELTA_Z);
            }
            else if (strcmp(tmpstr1, "DIMENSION") == 0)
            {
                simDomain->DIMENSION = atoi(tmpstr2);
                fprintf(fp, "%s = %ld\n", tmpstr1, simDomain->DIMENSION);
            }
            else if (strcmp(tmpstr1, "NUMPHASES") == 0)
            {
                simDomain->numPhases = atoi(tmpstr2);
                fprintf(fp, "%s = %ld\n", tmpstr1, simDomain->numPhases);
            }
            else if (strcmp(tmpstr1, "NUMCOMPONENTS") == 0)
            {
                simDomain->numComponents = atoi(tmpstr2);
                fprintf(fp, "%s = %ld\n", tmpstr1, simDomain->numComponents);
            }
            else if (strcmp(tmpstr1, "PHASES") == 0)
            {
                simDomain->phaseNames = (char**)malloc(sizeof(char*)*simDomain->numPhases);
                simDomain->phase_map = (char**)malloc(sizeof(char*)*simDomain->numPhases);

                simDomain->thermo_phase_host = (long*)malloc(sizeof(long)*simDomain->numPhases);
                cudaMalloc((void**)&simDomain->thermo_phase_dev, sizeof(long)*simDomain->numPhases);

                for (long i = 0; i < simDomain->numPhases; i++)
                {
                    simDomain->phaseNames[i] = (char*)malloc(sizeof(char)*30);
                    simDomain->phase_map[i] = (char*)malloc(sizeof(char)*30);
                }

                populate_string_array(simDomain->phaseNames, tmpstr2, simDomain->numPhases);
                ;
            }
            else if (strcmp(tmpstr1, "COMPONENTS") == 0)
            {
                simDomain->componentNames = (char**)malloc(sizeof(char*)*simDomain->numComponents);
                for (long i = 0; i < simDomain->numComponents; i++)
                    simDomain->componentNames[i] = (char*)malloc(sizeof(char)*30);

                populate_string_array(simDomain->componentNames, tmpstr2, simDomain->numComponents);

                if (simDomain->numComponents > 1 && simDomain->numPhases > 0)
                {
                    simParams->F0_Beq_host = MallocM(simDomain->numPhases, simDomain->numComponents-1);

                    simParams->DELTA_T = MallocM(simDomain->numPhases, simDomain->numPhases);
                    simParams->DELTA_C = MallocM(simDomain->numPhases, simDomain->numComponents-1);

                    simParams->dcbdT = Malloc3M(simDomain->numPhases, simDomain->numPhases, simDomain->numComponents-1);
                    simParams->dBbdT = MallocM(simDomain->numPhases, simDomain->numComponents-1);

                    simParams->slopes = Malloc3M(simDomain->numPhases, simDomain->numPhases, simDomain->numPhases);

                    simParams->gamma_host = MallocM(simDomain->numPhases, simDomain->numPhases);
                    cudaMalloc((void**)&simParams->gamma_dev, sizeof(double)*simDomain->numPhases*simDomain->numPhases);

                    simParams->Tau_host = MallocM(simDomain->numPhases, simDomain->numPhases);

                    simParams->relax_coeff_host = MallocM(simDomain->numPhases, simDomain->numPhases);
                    cudaMalloc((void**)&simParams->relax_coeff_dev, sizeof(double)*simDomain->numPhases*simDomain->numPhases);

                    simParams->kappaPhi_host = MallocM(simDomain->numPhases, simDomain->numPhases);
                    cudaMalloc((void**)&simParams->kappaPhi_dev, sizeof(double)*simDomain->numPhases*simDomain->numPhases);

                    simParams->diffusivity_host = Malloc3M(simDomain->numPhases, simDomain->numComponents-1, simDomain->numComponents-1);
                    cudaMalloc((void**)&(simParams->diffusivity_dev), sizeof(double)*simDomain->numPhases*(simDomain->numComponents-1)*(simDomain->numComponents-1));

                    simParams->mobility_host = Malloc3M(simDomain->numPhases, simDomain->numComponents-1, simDomain->numComponents-1);
                    cudaMalloc((void**)&(simParams->mobility_dev), sizeof(double)*simDomain->numPhases*(simDomain->numComponents-1)*(simDomain->numComponents-1));

                    simParams->F0_A_host = Malloc3M(simDomain->numPhases, simDomain->numComponents-1, simDomain->numComponents-1);
                    cudaMalloc((void**)&(simParams->F0_A_dev), sizeof(double)*simDomain->numPhases*(simDomain->numComponents-1)*(simDomain->numComponents-1));

                    simParams->F0_B_host = MallocM(simDomain->numPhases, simDomain->numComponents-1);
                    cudaMalloc((void**)&(simParams->F0_B_dev), sizeof(double)*simDomain->numPhases*(simDomain->numComponents-1));

                    simParams->F0_C_host = (double*)malloc(sizeof(double)*simDomain->numPhases);
                    cudaMalloc((void**)&(simParams->F0_C_dev), sizeof(double)*simDomain->numPhases);

                    simParams->ceq_host = Malloc3M(simDomain->numPhases, simDomain->numPhases, simDomain->numComponents-1);
                    cudaMalloc((void**)&(simParams->ceq_dev), sizeof(double)*simDomain->numPhases*simDomain->numPhases*(simDomain->numComponents-1));

                    simParams->cfill_host = Malloc3M(simDomain->numPhases, simDomain->numPhases, simDomain->numComponents-1);
                    cudaMalloc((void**)&(simParams->cfill_dev), sizeof(double)*simDomain->numPhases*simDomain->numPhases*(simDomain->numComponents-1));

                    simParams->cguess_host = Malloc3M(simDomain->numPhases, simDomain->numPhases, simDomain->numComponents-1);
                    cudaMalloc((void**)&(simParams->cguess_dev), sizeof(double)*simDomain->numPhases*simDomain->numPhases*(simDomain->numComponents-1));

                    simParams->theta_ijk_host = Malloc3M(simDomain->numPhases, simDomain->numPhases, simDomain->numPhases);

                    for (long i = 0; i < simDomain->numPhases; i++)
                        for (long j = 0; j < simDomain->numPhases; j++)
                            for (long k = 0; k < simDomain->numPhases; k++)
                                simParams->theta_ijk_host[i][j][k] = 0.0;
                    cudaMalloc((void**)&(simParams->theta_ijk_dev), sizeof(double)*simDomain->numPhases*simDomain->numPhases*simDomain->numPhases);

                    simParams->theta_ij_host = MallocM(simDomain->numPhases, simDomain->numPhases);
                    cudaMalloc((void**)&(simParams->theta_ij_dev), sizeof(double)*simDomain->numPhases*simDomain->numPhases);

                    simParams->theta_i_host = (double*)malloc(sizeof(double)*simDomain->numPhases);
                    cudaMalloc((void**)&(simParams->theta_i_dev), sizeof(double)*simDomain->numPhases);

                    simParams->Rotation_matrix_host = Malloc4M(simDomain->numPhases, simDomain->numPhases, 3, 3);
                    cudaMalloc((void**)&(simParams->Rotation_matrix_dev), sizeof(double)*simDomain->numPhases*simDomain->numPhases*3*3);

                    simParams->Inv_Rotation_matrix_host = Malloc4M(simDomain->numPhases, simDomain->numPhases, 3, 3);
                    cudaMalloc((void**)&(simParams->Inv_Rotation_matrix_dev), sizeof(double)*simDomain->numPhases*simDomain->numPhases*3*3);

                    for (long i = 0; i < 6; i++)
                    {
                        simControls->boundary[i] = (bc_scalars*)malloc(4*sizeof(*simControls->boundary[i])); //4=Number of scalar fields
                    }
                }
                else
                    printf("Invalid number of components and/or phases\n");
            }


            else if (strcmp(tmpstr1, "DELTA_t") == 0)
            {
                simControls->DELTA_t = atof(tmpstr2);
                fprintf(fp, "%s = %le\n", tmpstr1, simControls->DELTA_t);
            }
            else if (strcmp(tmpstr1, "RESTART") == 0)
            {
                simControls->restart = atol(tmpstr2);
            }
            else if (strcmp(tmpstr1, "STARTTIME") == 0)
            {
                simControls->startTime = atol(tmpstr2);
                fprintf(fp, "%s = %ld\n", tmpstr1, simControls->startTime);
                simControls->count = simControls->startTime;
            }
            else if (strcmp(tmpstr1, "NTIMESTEPS") == 0)
            {
                simControls->numSteps = atol(tmpstr2);
                fprintf(fp, "%s = %ld\n", tmpstr1, simControls->numSteps);
            }
            else if (strcmp(tmpstr1, "NSMOOTH") == 0)
            {
                simControls->nsmooth = atol(tmpstr2);
                fprintf(fp, "%s = %ld\n", tmpstr1, simControls->nsmooth);
            }
            else if (strcmp(tmpstr1, "SAVET") == 0)
            {
                simControls->saveInterval = atol(tmpstr2);
                fprintf(fp, "%s = %ld\n", tmpstr1, simControls->saveInterval);
            }
            else if (strcmp(tmpstr1, "TRACK_PROGRESS") == 0)
            {
                simControls->trackProgress = atol(tmpstr2);
                fprintf(fp, "%s = %ld\n", tmpstr1, simControls->trackProgress);
            }
            else if (strcmp(tmpstr1, "WRITEFORMAT") == 0)
            {
                if (strcmp(tmpstr2, "ASCII") == 0)
                    simControls->writeFormat = 1;
                else if (strcmp(tmpstr2, "BINARY") == 0)
                    simControls->writeFormat = 0;
                else
                    simControls->writeFormat = 2;
                fprintf(fp, "%s = %ld\n", tmpstr1, simControls->writeFormat);
            }
            else if (strcmp(tmpstr1, "WRITEHDF5") == 0)
            {
                simControls->writeHDF5 = atoi(tmpstr2);
                fprintf(fp, "%s = %ld\n", tmpstr1, simControls->writeHDF5);
            }

            else if (strcmp(tmpstr1, "GAMMA") == 0)
            {
                if (simDomain->numPhases > 0)
                    populate_matrix(simParams->gamma_host, tmpstr2, simDomain->numPhases);

                fprintf(fp, "%s = %le\n", tmpstr1, simParams->gamma_host[1][0]);
            }
            else if (strcmp(tmpstr1, "DIFFUSIVITY") == 0)
            {
                populate_diffusivity_matrix(simParams->diffusivity_host, tmpstr2, simDomain->numComponents);
            }
            else if (strcmp(tmpstr1, "Tau") == 0)
            {
                if (simDomain->numPhases > 0)
                    populate_matrix(simParams->Tau_host, tmpstr2, simDomain->numPhases);

                fprintf(fp, "%s = %le\n", tmpstr1, simParams->Tau_host[0][1]);
            }
            else if (strcmp(tmpstr1, "alpha") == 0)
            {
                simParams->alpha = atof(tmpstr2);
                fprintf(fp, "%s = %le\n", tmpstr1, simParams->alpha);
            }
            else if (strcmp(tmpstr1, "epsilon") == 0)
            {
                simParams->epsilon = atof(tmpstr2);
                fprintf(fp, "%s = %le\n", tmpstr1, simParams->epsilon);
            }
            else if (strcmp(tmpstr1, "ceq") == 0)
            {
                populate_thermodynamic_matrix(simParams->ceq_host, tmpstr2, simDomain->numComponents);
            }
            else if (strcmp(tmpstr1, "cfill") == 0)
            {
                populate_thermodynamic_matrix(simParams->cfill_host, tmpstr2, simDomain->numComponents);
            }
            else if (strcmp(tmpstr1, "c_guess") == 0)
            {
                populate_thermodynamic_matrix(simParams->cguess_host, tmpstr2, simDomain->numComponents);
            }
            else if (strcmp(tmpstr1, "R") == 0)
            {
                simParams->R = atof(tmpstr2);
                fprintf(fp, "%s = %le\n", tmpstr1, simParams->R);
            }
            else if (strcmp(tmpstr1, "V") == 0)
            {
                simParams->molarVolume = atof(tmpstr2);
                fprintf(fp, "%s = %le\n", tmpstr1, simParams->molarVolume);
            }
            else if (strcmp(tmpstr1, "T") == 0)
            {
                simParams->T = atof(tmpstr2);
                fprintf(fp, "%s = %le\n", tmpstr1, simParams->T);
            }
            else if (strcmp(tmpstr1, "Equilibrium_temperature") == 0)
            {
                simParams->Teq = atof(tmpstr2);
                fprintf(fp, "%s = %le\n", tmpstr1, simParams->Teq);
            }
            else if (strcmp(tmpstr1, "Filling_temperature") == 0)
            {
                simParams->Tfill = atof(tmpstr2);
                fprintf(fp, "%s = %le\n", tmpstr1, simParams->Tfill);
            }
            else if ((strcmp(tmpstr1, "Function_F") == 0) && simDomain->numPhases > 1 && simDomain->numComponents-1 > 0)
            {
                simControls->FUNCTION_F = atoi(tmpstr2);
                fprintf(fp, "%s = %ld\n", tmpstr1, simControls->FUNCTION_F);
            }
            else if (strcmp(tmpstr1, "A") == 0)
            {
                populate_A_matrix(simParams->F0_A_host, tmpstr2, simDomain->numComponents);
            }
            else if ((strcmp(tmpstr1, "tdbfname") == 0) && (simDomain->numPhases > 1));
            else if (strcmp(tmpstr1, "num_thermo_phases") == 0) {
                simDomain->numThermoPhases = atoi(tmpstr2);
                simDomain->phases_tdb = (char**)malloc(sizeof(char*)*simDomain->numThermoPhases);

                for(long i = 0; i < simDomain->numThermoPhases; i++)
                    simDomain->phases_tdb[i] = (char*)malloc(sizeof(char)*51);
            }
            else if (strcmp(tmpstr1, "tdb_phases")==0  && simDomain->numThermoPhases > 0) {
                populate_string_array(simDomain->phases_tdb, tmpstr2, simDomain->numThermoPhases);
            }
            else if (strcmp(tmpstr1, "phase_map")==0 && simDomain->numPhases > 1) {
                populate_string_array(simDomain->phase_map, tmpstr2, simDomain->numPhases);
            }
            else if (strcmp(tmpstr1, "theta_i")==0 && simDomain->numPhases > 1)
            {
                populate_thetai_matrix(simParams->theta_i_host, tmpstr2, simDomain->numPhases);
            }
            else if (strcmp(tmpstr1, "theta_ij") == 0 && simDomain->numPhases > 1)
            {
                populate_thetaij_matrix(simParams->theta_ij_host, tmpstr2, simDomain->numPhases);
            }
            else if (strcmp(tmpstr1, "Gamma_abc") == 0 && simDomain->numPhases > 1)
            {
                populate_matrix3M(simParams->theta_ijk_host, tmpstr2, simDomain->numPhases);
            }
            else if (strcmp(tmpstr1, "ISOTHERMAL") == 0)
            {
                simControls->ISOTHERMAL = atoi(tmpstr2);
            }
            else if (strcmp(tmpstr1, "dTdt") == 0 && simDomain->numPhases > 1)
            {
                simControls->dTdt = atof(tmpstr2);
                fprintf(fp, "%s = %le\n", tmpstr1, simControls->dTdt);
            }
            else if (strcmp(tmpstr1, "T_update") == 0 && simDomain->numPhases > 1)
            {
                simControls->T_update = atoi(tmpstr2);
                fprintf(fp, "%s = %ld\n", tmpstr1, simControls->T_update);
            }
            else if (strcmp(tmpstr1, "SEED") == 0)
            {
                simParams->SEED = atol(tmpstr2);
                fprintf(fp, "%s = %ld\n", tmpstr1, simParams->SEED);
            }
            else if (strcmp(tmpstr1, "Function_anisotropy") == 0)
            {
                simControls->FUNCTION_ANISOTROPY = atoi(tmpstr2);
            }
            else if ((strcmp(tmpstr1, "Anisotropy_type") == 0) && (simControls->FUNCTION_ANISOTROPY != 0))
            {
                simControls->FOLD = atoi(tmpstr2);
            }
            else if ((strcmp(tmpstr1, "Rotation_matrix") == 0) && (simControls->FUNCTION_ANISOTROPY != 0))
            {
                populate_rotation_matrix(simParams->Rotation_matrix_host, simParams->Inv_Rotation_matrix_host, tmpstr2);
            }
            else if (strcmp(tmpstr1, "dab") == 0)
            {
                simParams->dab_host = MallocM(simDomain->numPhases, simDomain->numPhases);
                cudaMalloc((void**)&(simParams->dab_dev), sizeof(double)*simDomain->numPhases*simDomain->numPhases);
                populate_matrix(simParams->dab_host, tmpstr2, simDomain->numPhases);
            }
          //  else if (rank == 1)
               // printf("Unrecognized parameter : \"%s\"\n", tmpstr1);
        }
    }

    if (simControls->writeHDF5 == 1)
        simControls->writeFormat = 2;

    fprintf(fp, "ceq\n");
    for (long i = 0; i < simDomain->numPhases; i++)
    {
        for (long j = 0; j < simDomain->numPhases; j++)
        {
            for (long k = 0; k < simDomain->numComponents-1; k++)
            {
                fprintf(fp, "%ld %ld %ld\t%le\t", i, j, k, simParams->ceq_host[i][j][k]);
            }
        }
        fprintf(fp, "\n");
    }

    fclose(fr);
    fclose(fp);
}
