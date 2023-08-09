/* The testJNI.c file, which implements the native function */
#include <jni.h>      /* Java Native Interface headers */
#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>
#include <time.h>

#include "com_jni_daq.h"   /* Auto-generated header created by javah -jni*/

#include "NIDAQmx.h"

#define GPISIZE 255
#define NUMGPIS 5
#define DAQmxErrChk(functionCall) { if( DAQmxFailed(error=(functionCall)) ) { goto Error; } }

static gpiSize = GPISIZE;
static numGPIs = NUMGPIS;

/*Initialise TaskHandle to 0 to begin with - value MUST change for each port on each DAQ device */
TaskHandle	taskHandle=0;
uInt32		data;
int32		read;

static int initialised = 0;

static	char	staticTest[255];

static	gpiVal[NUMGPIS][GPISIZE];

JNIEXPORT jstring JNICALL
Java_com_jni_daq_testJNI(JNIEnv *env, jobject obj, jstring jstr)
{
  char *str = (*env)->GetStringUTFChars(env, jstr, 0);
  strcpy(staticTest, str);
  (*env)->ReleaseStringUTFChars(env, jstr, str);
//  staticTest = jstring;
  return (*env)->NewStringUTF(env, staticTest);
}

JNIEXPORT jint JNICALL Java_com_jni_daq_initializeDAQ(JNIEnv *env, jobject obj, jstring jstr)
{
	int32		error=0;
	int32		i=0;
    char        devAndPortNum[50];
    uInt32		data;
	//uInt32		serNum;
	char		errBuff[2048]={'\0'};
	/* Put the device string into a devNum char array */
	char *str = (*env)->GetStringUTFChars(env, jstr, 0);
	int32		read;
	
    strcpy(devAndPortNum, str);
    (*env)->ReleaseStringUTFChars(env, jstr, str);



	/*********************************************/
	/*/ DAQmx Configure Code
	/*********************************************/
	DAQmxCreateTask("",&taskHandle);
	DAQmxCreateDIChan(taskHandle,devAndPortNum,"",DAQmx_Val_ChanForAllLines);
	//DAQmxErrChk (DAQmxGetDevSerialNum("Dev2/port2", &serNum));

	/*********************************************/
	/*/ DAQmx Start Code
	/*********************************************/
	DAQmxStartTask(taskHandle);

	return (taskHandle);
}



JNIEXPORT jstring JNICALL
Java_com_jni_daq_closeDAQ(JNIEnv *env, jobject obj, jint taskHandle)
{
		DAQmxStopTask(taskHandle);
		DAQmxClearTask(taskHandle);
  return (*env)->NewStringUTF(env, staticTest);
}

JNIEXPORT jstring JNICALL
Java_com_jni_daq_registerOnGPI(JNIEnv *env, jobject obj, jstring jstr)
{
  /* Call Y0(x) Bessel function from standard C mathematical library */
//  y = y0(x);
  return (*env)->NewStringUTF(env, staticTest);
}


JNIEXPORT jint JNICALL 
Java_com_jni_daq_pollGPI (JNIEnv *, jobject, jint);

JNIEXPORT jint JNICALL
Java_com_jni_daq_pollGPI(JNIEnv *env, jobject obj, jint gpiPortTaskHandle)
{
	taskHandle = gpiPortTaskHandle;
	DAQmxReadDigitalU32(taskHandle,1,10.0,DAQmx_Val_GroupByChannel,&data,1,&read,NULL);
	return data;
}
JNIEXPORT void JNICALL 
Java_com_jni_daq_setCallback(JNIEnv *env, jobject obj, jint depth)
{
  jclass cls = (*env)->GetObjectClass(env, obj);
  jmethodID mid = (*env)->GetMethodID(env, cls, "callback", "(I)V");
  if (mid == 0) {
    return;
  }
  printf("In C, depth = %d, about to enter Java\n", depth);
  (*env)->CallVoidMethod(env, obj, mid, depth);
  printf("In C, depth = %d, back from Java\n", depth);
}

JNIEXPORT jint JNICALL
Java_com_jni_daq_retrieveSerialNumber(JNIEnv *env, jobject obj, jstring jstr)
{
	char        devNum[50];
	uInt32 serNum;

	char *str = (*env)->GetStringUTFChars(env, jstr, 0);
	strcpy(devNum, str);
	//printf("%s", str);
	(*env)->ReleaseStringUTFChars(env, jstr, str);
	// jstring = staticTest

	DAQmxGetDevSerialNum(devNum,&serNum);
	//printf("Serial number: %X\n", serNum); 
	return serNum;
}
