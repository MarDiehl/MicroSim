

void CL_Solve_phi_com_Function_F_2(long t) {
  //printf("F 2 \n");
  tstep[0] = t;
  ret  = clEnqueueWriteBuffer(cmdQ, d_tstep, CL_TRUE, 0, sizeof(long), tstep, 0, NULL, NULL);
  if (ret!=CL_SUCCESS) {
    printf("enq buffer write error d_tstep %d\n", ret);
    exit(1);
  }
    
  if ( (t > tNoiseStart) && (FUNCTION_ANISOTROPY == 1) ) { 
    ret = clEnqueueNDRangeKernel(cmdQ, kernel8, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    if (ret!=CL_SUCCESS) {
      printf("kernel8 enq problem  %d\n",ret);
      exit(1);
    }
  }

  ret = clEnqueueNDRangeKernel(cmdQ, kernel9, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  if (ret!=CL_SUCCESS) {
    printf("kernel9 enq problem  %d\n",ret);
    exit(1);
  }
  
  ret = clEnqueueNDRangeKernel(cmdQ, kernel1_2, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  if (ret!=CL_SUCCESS) {
    printf("kernel1_2 enq problem  %d in rank = %d \n",ret, rank);
    exit(1);
  }
  
  if ( (t > nsmooth) && (FUNCTION_ANISOTROPY == 1) ) {
    
    ret = clEnqueueNDRangeKernel(cmdQ, kernel2b_2, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    if (ret!=CL_SUCCESS) {
      printf("kernel2b_2 enq problem  %d in rank = %d \n",ret, rank);
      exit(1);
    }
    
  }
  else {
    
    ret = clEnqueueNDRangeKernel(cmdQ, kernel2a_2, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    if (ret!=CL_SUCCESS) {
      printf("kernel2a_2 enq problem  %d in rank = %d \n",ret, rank);
      exit(1);
    }
    
  }

  if ( boundary[0][0].type == 1 ) { 
    ret  = clEnqueueNDRangeKernel(cmdQ, kernel6[1], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else if ( boundary[0][0].type == 3 ) {
    ret  = clEnqueueNDRangeKernel(cmdQ, kernel6[3], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else {
    printf("No Boundary condition for X (left and right) \n");
    exit(1);
  }
  if (ret!=CL_SUCCESS) {
    printf("kernel6j enq problem  %d\n",ret);
    exit(1);
  }

  if ( boundary[1][0].type == 1 ) {
    ret |= clEnqueueNDRangeKernel(cmdQ, kernel6[2], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else if ( boundary[1][0].type == 3 ) {
    ret |= clEnqueueNDRangeKernel(cmdQ, kernel6[4], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else {
    printf("No Boundary condition for X (left and right) \n");
    exit(1);
  }
  if (ret!=CL_SUCCESS) {
    printf("kernel6j enq problem  %d\n",ret);
    exit(1);
  }

  if ( boundary[2][0].type == 1 ) {
    ret = clEnqueueNDRangeKernel(cmdQ, kernel6[5], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else if ( boundary[2][0].type == 3 ) {
    ret = clEnqueueNDRangeKernel(cmdQ, kernel6[7], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else {
    printf("No Boundary condition for Y (top and bottom) \n");
    exit(1);
  }
  if (ret!=CL_SUCCESS) {
    printf("kernel6i enq problem  %d\n",ret);
    exit(1);
  }

  if ( boundary[3][0].type == 1 ) {
    ret = clEnqueueNDRangeKernel(cmdQ, kernel6[6], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else if ( boundary[3][0].type == 3 ) {
    ret = clEnqueueNDRangeKernel(cmdQ, kernel6[8], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else {
    printf("No Boundary condition for Y (top and bottom) \n");
    exit(1);
  }
  if (ret!=CL_SUCCESS) {
    printf("kernel6i enq problem  %d\n",ret);
    exit(1);
  }

  if ( (t > nsmooth) && atr ) {
    
    ret = clEnqueueNDRangeKernel(cmdQ, kernel3b_2, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    if (ret!=CL_SUCCESS) {
      printf("kernel3b_2 enq problem  %d\n",ret);
      exit(1);
    }
    
  }
  else {
    
    
    ret = clEnqueueNDRangeKernel(cmdQ, kernel3a_2, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    if (ret!=CL_SUCCESS) {
      printf("kernel3a_2 enq problem  %d\n",ret);
      exit(1);
    }
    
  }

  if ( boundary[0][1].type == 1 ) {
    ret  = clEnqueueNDRangeKernel(cmdQ, kernel7[1], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else if ( boundary[0][1].type == 3 ) {
    ret  = clEnqueueNDRangeKernel(cmdQ, kernel7[3], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else {
    printf("No Boundary condition for X (left and right) \n");
    exit(1);
  }
  if (ret!=CL_SUCCESS) {
    printf("kernel7j enq problem  %d\n",ret);
    exit(1);
  }

  if ( boundary[1][1].type == 1 ) {
    ret |= clEnqueueNDRangeKernel(cmdQ, kernel7[2], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else if ( boundary[1][1].type == 3 ) {
    ret |= clEnqueueNDRangeKernel(cmdQ, kernel7[4], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else {
    printf("No Boundary condition for X (left and right) \n");
    exit(1);
  }
  if (ret!=CL_SUCCESS) {
    printf("kernel7j enq problem  %d\n",ret);
    exit(1);
  }

  if ( boundary[2][1].type == 1 ) { 
    ret = clEnqueueNDRangeKernel(cmdQ, kernel7[5], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else if ( boundary[2][1].type == 3 ) {
    ret = clEnqueueNDRangeKernel(cmdQ, kernel7[7], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else {
    printf("No Boundary condition for Y (top and bottom) \n");
    exit(1);
  }
  if (ret!=CL_SUCCESS) {
    printf("kernel7i enq problem  %d\n",ret);
    exit(1);
  }
  
  if ( boundary[3][1].type == 1 ) { 
    ret = clEnqueueNDRangeKernel(cmdQ, kernel7[6], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else if ( boundary[3][1].type == 3 ) { 
    ret = clEnqueueNDRangeKernel(cmdQ, kernel7[8], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else {
    printf("No Boundary condition for Y (top and bottom) \n");
    exit(1);
  }
  if (ret!=CL_SUCCESS) {
    printf("kernel7i enq problem  %d\n",ret);
    exit(1);
  }
  
}


void CL_Solve_phi_com_Function_F_3(long t) {
  //printf("F 3 \n");
  tstep[0] = t;
  ret  = clEnqueueWriteBuffer(cmdQ, d_tstep, CL_TRUE, 0, sizeof(long), tstep, 0, NULL, NULL);
  if (ret!=CL_SUCCESS) {
    printf("enq buffer write error d_tstep %d\n", ret);
    exit(1);
  }
    
  if ( (t > tNoiseStart) && (FUNCTION_ANISOTROPY == 1) ) { 
    ret = clEnqueueNDRangeKernel(cmdQ, kernel8, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    if (ret!=CL_SUCCESS) {
      printf("kernel8 enq problem  %d\n",ret);
      exit(1);
    }
  }

  ret = clEnqueueNDRangeKernel(cmdQ, kernel9, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  if (ret!=CL_SUCCESS) {
    printf("kernel9 enq problem  %d\n",ret);
    exit(1);
  }

  // ret = clEnqueueNDRangeKernel(cmdQ, kernel1, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  // if (ret!=CL_SUCCESS) {
  //   printf("kernel1 enq problem  %d in rank = %d \n",ret, rank);
  //   exit(1);
  // }

  // ret = clEnqueueNDRangeKernel(cmdQ, kernel1_2, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  // if (ret!=CL_SUCCESS) {
  //   printf("kernel1_2 enq problem  %d in rank = %d \n",ret, rank);
  //   exit(1);
  // }

  ret = clEnqueueNDRangeKernel(cmdQ, kernel1_3, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  if (ret!=CL_SUCCESS) {
    printf("kernel1_3 enq problem  %d in rank = %d \n",ret, rank);
    exit(1);
  }
  
  if ( (t > nsmooth) && (FUNCTION_ANISOTROPY == 1) ) {
    // ret = clEnqueueNDRangeKernel(cmdQ, kernel2b, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    // if (ret!=CL_SUCCESS) {
    //   printf("kernel2b enq problem  %d in rank = %d \n",ret, rank);
    //   exit(1);
    // }

    // ret = clEnqueueNDRangeKernel(cmdQ, kernel2b_2, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    // if (ret!=CL_SUCCESS) {
    //   printf("kernel2b_2 enq problem  %d in rank = %d \n",ret, rank);
    //   exit(1);
    // }

    ret = clEnqueueNDRangeKernel(cmdQ, kernel2b_3, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    if (ret!=CL_SUCCESS) {
      printf("kernel2b_3 enq problem  %d in rank = %d \n",ret, rank);
      exit(1);
    }
  }
  else {
    // ret = clEnqueueNDRangeKernel(cmdQ, kernel2a, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    // if (ret!=CL_SUCCESS) {
    //   printf("kernel2a enq problem  %d in rank = %d \n",ret, rank);
    //   exit(1);
    // }
    
    // ret = clEnqueueNDRangeKernel(cmdQ, kernel2a_2, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    // if (ret!=CL_SUCCESS) {
    //   printf("kernel2a_2 enq problem  %d in rank = %d \n",ret, rank);
    //   exit(1);
    // }
    
    ret = clEnqueueNDRangeKernel(cmdQ, kernel2a_3, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    if (ret!=CL_SUCCESS) {
      printf("kernel2a_3 enq problem  %d in rank = %d \n",ret, rank);
      exit(1);
    }
  }

  if ( boundary[0][0].type == 1 ) { 
    ret  = clEnqueueNDRangeKernel(cmdQ, kernel6[1], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else if ( boundary[0][0].type == 3 ) {
    ret  = clEnqueueNDRangeKernel(cmdQ, kernel6[3], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else {
    printf("No Boundary condition for X (left and right) \n");
    exit(1);
  }
  if (ret!=CL_SUCCESS) {
    printf("kernel6j enq problem  %d\n",ret);
    exit(1);
  }

  if ( boundary[1][0].type == 1 ) {
    ret |= clEnqueueNDRangeKernel(cmdQ, kernel6[2], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else if ( boundary[1][0].type == 3 ) {
    ret |= clEnqueueNDRangeKernel(cmdQ, kernel6[4], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else {
    printf("No Boundary condition for X (left and right) \n");
    exit(1);
  }
  if (ret!=CL_SUCCESS) {
    printf("kernel6j enq problem  %d\n",ret);
    exit(1);
  }

  if ( boundary[2][0].type == 1 ) {
    ret = clEnqueueNDRangeKernel(cmdQ, kernel6[5], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else if ( boundary[2][0].type == 3 ) {
    ret = clEnqueueNDRangeKernel(cmdQ, kernel6[7], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else {
    printf("No Boundary condition for Y (top and bottom) \n");
    exit(1);
  }
  if (ret!=CL_SUCCESS) {
    printf("kernel6i enq problem  %d\n",ret);
    exit(1);
  }

  if ( boundary[3][0].type == 1 ) {
    ret = clEnqueueNDRangeKernel(cmdQ, kernel6[6], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else if ( boundary[3][0].type == 3 ) {
    ret = clEnqueueNDRangeKernel(cmdQ, kernel6[8], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else {
    printf("No Boundary condition for Y (top and bottom) \n");
    exit(1);
  }
  if (ret!=CL_SUCCESS) {
    printf("kernel6i enq problem  %d\n",ret);
    exit(1);
  }

  if ( (t > nsmooth) && atr ) {
    // ret = clEnqueueNDRangeKernel(cmdQ, kernel3b, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    // if (ret!=CL_SUCCESS) {
    //   printf("kernel3b enq problem  %d\n",ret);
    //   exit(1);
    // }

    // ret = clEnqueueNDRangeKernel(cmdQ, kernel3b_2, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    // if (ret!=CL_SUCCESS) {
    //   printf("kernel3b_2 enq problem  %d\n",ret);
    //   exit(1);
    // }

    ret = clEnqueueNDRangeKernel(cmdQ, kernel3b_3, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    if (ret!=CL_SUCCESS) {
      printf("kernel3b_3 enq problem  %d\n",ret);
      exit(1);
    }
  }
  else {
    // ret = clEnqueueNDRangeKernel(cmdQ, kernel3a, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    // if (ret!=CL_SUCCESS) {
    //   printf("kernel3a enq problem  %d\n",ret);
    //   exit(1);
    // }
    
    // ret = clEnqueueNDRangeKernel(cmdQ, kernel3a_2, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    // if (ret!=CL_SUCCESS) {
    //   printf("kernel3a_2 enq problem  %d\n",ret);
    //   exit(1);
    // }
    
    ret = clEnqueueNDRangeKernel(cmdQ, kernel3a_3, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    if (ret!=CL_SUCCESS) {
      printf("kernel3a_3 enq problem  %d\n",ret);
      exit(1);
    }
  }

  if ( boundary[0][1].type == 1 ) {
    ret  = clEnqueueNDRangeKernel(cmdQ, kernel7[1], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else if ( boundary[0][1].type == 3 ) {
    ret  = clEnqueueNDRangeKernel(cmdQ, kernel7[3], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else {
    printf("No Boundary condition for X (left and right) \n");
    exit(1);
  }
  if (ret!=CL_SUCCESS) {
    printf("kernel7j enq problem  %d\n",ret);
    exit(1);
  }

  if ( boundary[1][1].type == 1 ) {
    ret |= clEnqueueNDRangeKernel(cmdQ, kernel7[2], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else if ( boundary[1][1].type == 3 ) {
    ret |= clEnqueueNDRangeKernel(cmdQ, kernel7[4], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else {
    printf("No Boundary condition for X (left and right) \n");
    exit(1);
  }
  if (ret!=CL_SUCCESS) {
    printf("kernel7j enq problem  %d\n",ret);
    exit(1);
  }

  if ( boundary[2][1].type == 1 ) { 
    ret = clEnqueueNDRangeKernel(cmdQ, kernel7[5], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else if ( boundary[2][1].type == 3 ) {
    ret = clEnqueueNDRangeKernel(cmdQ, kernel7[7], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else {
    printf("No Boundary condition for Y (top and bottom) \n");
    exit(1);
  }
  if (ret!=CL_SUCCESS) {
    printf("kernel7i enq problem  %d\n",ret);
    exit(1);
  }
  
  if ( boundary[3][1].type == 1 ) { 
    ret = clEnqueueNDRangeKernel(cmdQ, kernel7[6], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else if ( boundary[3][1].type == 3 ) { 
    ret = clEnqueueNDRangeKernel(cmdQ, kernel7[8], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else {
    printf("No Boundary condition for Y (top and bottom) \n");
    exit(1);
  }
  if (ret!=CL_SUCCESS) {
    printf("kernel7i enq problem  %d\n",ret);
    exit(1);
  }
  
}




void CL_Solve_phi_com_Function_F_4(long t) {

  tstep[0] = t;
  ret  = clEnqueueWriteBuffer(cmdQ, d_tstep, CL_TRUE, 0, sizeof(long), tstep, 0, NULL, NULL);
  if (ret!=CL_SUCCESS) {
    printf("enq buffer write error d_tstep %d\n", ret);
    exit(1);
  }
  
  if ( !ISOTHERMAL ) { 
    ret = clEnqueueReadBuffer(cmdQ, d_temp, CL_TRUE, 0, nx*sizeof(double), temp, 0, NULL, NULL);// Changed to nx for MESH_Y
    if (ret != CL_SUCCESS) {
      printf("Error: Failed to read d_temp \n%d\n", ret);
      exit(1);
    }
    
    FunctionF_4_SplineCPU(propf4spline, temp, 0);
    
    ret  = clEnqueueWriteBuffer(cmdQ, d_propf4spline, CL_TRUE, 0, nx*sizeof(struct propmatf4spline), propf4spline, 0, NULL, NULL);
    if (ret!=CL_SUCCESS) {
      printf("enq buffer write error d_propf4spline %d\n", ret);
      exit(1);
    }
    
    FunctionF_4_SplineCPU(propf4spline1, temp, 1);
    
    ret  = clEnqueueWriteBuffer(cmdQ, d_propf4spline1, CL_TRUE, 0, nx*sizeof(struct propmatf4spline), propf4spline1, 0, NULL, NULL);
    if (ret!=CL_SUCCESS) {
      printf("enq buffer write error d_propf4spline1 %d\n", ret);
      exit(1);
    }
    
  }
    

  if ( (t > tNoiseStart) && (FUNCTION_ANISOTROPY == 1) ) { 
    ret = clEnqueueNDRangeKernel(cmdQ, kernel8, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    if (ret!=CL_SUCCESS) {
      printf("kernel8 enq problem  %d\n",ret);
      exit(1);
    }
  }

  ret = clEnqueueNDRangeKernel(cmdQ, kernel9, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  if (ret!=CL_SUCCESS) {
    printf("kernel9 enq problem  %d\n",ret);
    exit(1);
  }

  // ret = clEnqueueNDRangeKernel(cmdQ, kernel1, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  // if (ret!=CL_SUCCESS) {
  //   printf("kernel1 enq problem  %d in rank = %d \n",ret, rank);
  //   exit(1);
  // }

  // ret = clEnqueueNDRangeKernel(cmdQ, kernel1_2, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  // if (ret!=CL_SUCCESS) {
  //   printf("kernel1_2 enq problem  %d in rank = %d \n",ret, rank);
  //   exit(1);
  // }

  // ret = clEnqueueNDRangeKernel(cmdQ, kernel1_3, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  // if (ret!=CL_SUCCESS) {
  //   printf("kernel1_3 enq problem  %d in rank = %d \n",ret, rank);
  //   exit(1);
  // }

  ret = clEnqueueNDRangeKernel(cmdQ, kernel1_4, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  if (ret!=CL_SUCCESS) {
    printf("kernel1_4 enq problem  %d in rank = %d \n",ret, rank);
    exit(1);
  }
  
  if ( (t > nsmooth) && (FUNCTION_ANISOTROPY == 1) ) {
    // ret = clEnqueueNDRangeKernel(cmdQ, kernel2b, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    // if (ret!=CL_SUCCESS) {
    //   printf("kernel2b enq problem  %d in rank = %d \n",ret, rank);
    //   exit(1);
    // }
    
    // ret = clEnqueueNDRangeKernel(cmdQ, kernel2b_2, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    // if (ret!=CL_SUCCESS) {
    //   printf("kernel2b_2 enq problem  %d in rank = %d \n",ret, rank);
    //   exit(1);
    // }
    
    // ret = clEnqueueNDRangeKernel(cmdQ, kernel2b_3, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    // if (ret!=CL_SUCCESS) {
    //   printf("kernel2b_3 enq problem  %d in rank = %d \n",ret, rank);
    //   exit(1);
    // }
    
    ret = clEnqueueNDRangeKernel(cmdQ, kernel2b_4, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    if (ret!=CL_SUCCESS) {
      printf("kernel2b_4 enq problem  %d in rank = %d \n",ret, rank);
      exit(1);
    }
  }
  else {
    // ret = clEnqueueNDRangeKernel(cmdQ, kernel2a, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    // if (ret!=CL_SUCCESS) {
    //   printf("kernel2a enq problem  %d in rank = %d \n",ret, rank);
    //   exit(1);
    // }
    
    // ret = clEnqueueNDRangeKernel(cmdQ, kernel2a_2, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    // if (ret!=CL_SUCCESS) {
    //   printf("kernel2a_2 enq problem  %d in rank = %d \n",ret, rank);
    //   exit(1);
    // }
    
    // ret = clEnqueueNDRangeKernel(cmdQ, kernel2a_3, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    // if (ret!=CL_SUCCESS) {
    //   printf("kernel2a_3 enq problem  %d in rank = %d \n",ret, rank);
    //   exit(1);
    // }
    
    ret = clEnqueueNDRangeKernel(cmdQ, kernel2a_4, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    if (ret!=CL_SUCCESS) {
      printf("kernel2a_4 enq problem  %d in rank = %d \n",ret, rank);
      exit(1);
    }
  }

  if ( boundary[0][0].type == 1 ) { 
    ret  = clEnqueueNDRangeKernel(cmdQ, kernel6[1], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else if ( boundary[0][0].type == 3 ) {
    ret  = clEnqueueNDRangeKernel(cmdQ, kernel6[3], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else {
    printf("No Boundary condition for X (left and right) \n");
    exit(1);
  }
  if (ret!=CL_SUCCESS) {
    printf("kernel6j enq problem  %d\n",ret);
    exit(1);
  }

  if ( boundary[1][0].type == 1 ) {
    ret |= clEnqueueNDRangeKernel(cmdQ, kernel6[2], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else if ( boundary[1][0].type == 3 ) {
    ret |= clEnqueueNDRangeKernel(cmdQ, kernel6[4], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else {
    printf("No Boundary condition for X (left and right) \n");
    exit(1);
  }
  if (ret!=CL_SUCCESS) {
    printf("kernel6j enq problem  %d\n",ret);
    exit(1);
  }

  if ( boundary[2][0].type == 1 ) {
    ret = clEnqueueNDRangeKernel(cmdQ, kernel6[5], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else if ( boundary[2][0].type == 3 ) {
    ret = clEnqueueNDRangeKernel(cmdQ, kernel6[7], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else {
    printf("No Boundary condition for Y (top and bottom) \n");
    exit(1);
  }
  if (ret!=CL_SUCCESS) {
    printf("kernel6i enq problem  %d\n",ret);
    exit(1);
  }

  if ( boundary[3][0].type == 1 ) {
    ret = clEnqueueNDRangeKernel(cmdQ, kernel6[6], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else if ( boundary[3][0].type == 3 ) {
    ret = clEnqueueNDRangeKernel(cmdQ, kernel6[8], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else {
    printf("No Boundary condition for Y (top and bottom) \n");
    exit(1);
  }
  if (ret!=CL_SUCCESS) {
    printf("kernel6i enq problem  %d\n",ret);
    exit(1);
  }

  if ( (t > nsmooth) && atr ) {
    // ret = clEnqueueNDRangeKernel(cmdQ, kernel3b, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    // if (ret!=CL_SUCCESS) {
    //   printf("kernel3b enq problem  %d\n",ret);
    //   exit(1);
    // }
    
    // ret = clEnqueueNDRangeKernel(cmdQ, kernel3b_2, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    // if (ret!=CL_SUCCESS) {
    //   printf("kernel3b_2 enq problem  %d\n",ret);
    //   exit(1);
    // }
    
    // ret = clEnqueueNDRangeKernel(cmdQ, kernel3b_3, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    // if (ret!=CL_SUCCESS) {
    //   printf("kernel3b_3 enq problem  %d\n",ret);
    //   exit(1);
    // }

    ret = clEnqueueNDRangeKernel(cmdQ, kernel3b_4, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    if (ret!=CL_SUCCESS) {
      printf("kernel3b_4 enq problem  %d\n",ret);
      exit(1);
    }
  }
  else {
    // ret = clEnqueueNDRangeKernel(cmdQ, kernel3a, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    // if (ret!=CL_SUCCESS) {
    //   printf("kernel3a enq problem  %d\n",ret);
    //   exit(1);
    // }

    // ret = clEnqueueNDRangeKernel(cmdQ, kernel3a_2, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    // if (ret!=CL_SUCCESS) {
    //   printf("kernel3a_2 enq problem  %d\n",ret);
    //   exit(1);
    // }

    // ret = clEnqueueNDRangeKernel(cmdQ, kernel3a_3, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    // if (ret!=CL_SUCCESS) {
    //   printf("kernel3a_3 enq problem  %d\n",ret);
    //   exit(1);
    // }

    ret = clEnqueueNDRangeKernel(cmdQ, kernel3a_4, work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
    if (ret!=CL_SUCCESS) {
      printf("kernel3a_4 enq problem  %d\n",ret);
      exit(1);
    }
  }

  if ( boundary[0][1].type == 1 ) {
    ret  = clEnqueueNDRangeKernel(cmdQ, kernel7[1], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else if ( boundary[0][1].type == 3 ) {
    ret  = clEnqueueNDRangeKernel(cmdQ, kernel7[3], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else {
    printf("No Boundary condition for X (left and right) \n");
    exit(1);
  }
  if (ret!=CL_SUCCESS) {
    printf("kernel7j enq problem  %d\n",ret);
    exit(1);
  }

  if ( boundary[1][1].type == 1 ) {
    ret |= clEnqueueNDRangeKernel(cmdQ, kernel7[2], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else if ( boundary[1][1].type == 3 ) {
    ret |= clEnqueueNDRangeKernel(cmdQ, kernel7[4], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else {
    printf("No Boundary condition for X (left and right) \n");
    exit(1);
  }
  if (ret!=CL_SUCCESS) {
    printf("kernel7j enq problem  %d\n",ret);
    exit(1);
  }

  if ( boundary[2][1].type == 1 ) { 
    ret = clEnqueueNDRangeKernel(cmdQ, kernel7[5], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else if ( boundary[2][1].type == 3 ) {
    ret = clEnqueueNDRangeKernel(cmdQ, kernel7[7], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else {
    printf("No Boundary condition for Y (top and bottom) \n");
    exit(1);
  }
  if (ret!=CL_SUCCESS) {
    printf("kernel7i enq problem  %d\n",ret);
    exit(1);
  }
  
  if ( boundary[3][1].type == 1 ) { 
    ret = clEnqueueNDRangeKernel(cmdQ, kernel7[6], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else if ( boundary[3][1].type == 3 ) { 
    ret = clEnqueueNDRangeKernel(cmdQ, kernel7[8], work_dim, NULL, globaldim, NULL, 0, NULL, NULL);
  }
  else {
    printf("No Boundary condition for Y (top and bottom) \n");
    exit(1);
  }
  if (ret!=CL_SUCCESS) {
    printf("kernel7i enq problem  %d\n",ret);
    exit(1);
  }
  
}

