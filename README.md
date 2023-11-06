# taVNS CloseNIT Pilot Project
(transcutaneous auricular Vagus Nerve Stimulation)

## About

Co-morbid depression is common in people with heart failure (HF) and leads to worse health
outcomes. Autonomic nervous system (ANS) dysregulation, as indexed by reduced heart rate
variability (HRV), is seen in depression and HF. We hypothesise that ANS dysregulation is
mechanistically involved in depression in HF patients, explaining the poor prognosis. Implanted
vagus nerve stimulation (VNS) directly targets the ANS. It is used clinically in depression and
experimentally in HF, consistently improving quality of life (QoL). Transauricular VNS (taVNS) is a
non-invasive alternative. It holds promise but optimal stimulation parameters are not known. Our
collaboration has demonstrated the feasibility of open-loop taVNS and identified parameter-
specific effects on the HRV of healthy volunteers. The respiratory cycle is relevant for the effects
of taVNS on ANS modulation. We propose a proof-of-concept study to develop lab-based closed-
loop taVNS techniques, gated to trigger stimulation at specific points in the respiratory cycle of
healthy volunteers, to determine ANS impact on measures of electroencephalography (EEG), HRV,
blood pressure and continuous performance tests. In parallel we are studying ANS function,
mood, fatigue and QoL in people with depression and HF. Non-invasive ANS modulation is a potential novel therapeutic strategy targeting mood, fatigue and QoL in HF.

### Project Team
Dr Jannetta Steyn, Newcastle University  ([jannetta.steyn@newcastle.ac.uk](mailto:jannetta.steyn@newcastle.ac.uk))  
Dr Frances Turner, Newcastle University  ([frances.hutchings@newcastle.ac.uk](mailto:frances.hutchings@newcastle.ac.uk)) 
Dr. Tiago da Silva Costa, Newcastle University ([tiago.da-silva-costa@newcastle.ac.uk](mailto:tiago.da-silva-costa@newcastle.ac.uk))

### RSE Contacts
Frances & Jannetta  
RSE Team  
Newcastle University  
([frances.hutchings@newcastle.ac.uk](mailto:frances.hutchings@newcastle.ac.uk))  
([jannetta.steyn@newcastle.ac.uk](mailto:jannetta.steyn@newcastle.ac.uk))  

## Built With (Hardware)
DS8 Digitimer 
National Instruments USB-6229

Testing:
Oscillascope
Signal Generator


## Built With (Software)

Using code from the CCS-Lab DS8R\_python repository (https://github.com/CCS-Lab/DS8R\_python)

[Framework 3](https://something.com)  
## Getting Started

### Prerequisites

- Digistim DS8R
- AD Instruments PowerLab 4/26
- NI USB6229
- An oscilloscope would be handy
- An ESP32 microcontroller for running the breathing simulator would be handy

### Installation

Install the DS8R package:
```
# Install from GitHub
pip install -e git+https://github.com/CCS-Lab/DS8R_python#egg=ds8r
```


### Running Locally

This application is best run in a virtual environment such as `venv`. Make sure **Python 3**, **pip** and **venv**
are installed

### Running Tests

How to run tests on your local system.

## Deployment

### Local

Deploying to a production style setup but on the local system. Examples of this would include `venv`, `anaconda`, `Docker` or `minikube`. 

### Production

Deploying to the production system. Examples of this would include cloud, HPC or virtual machine. 

## Usage

Any links to production environment, video demos and screenshots.

## Roadmap

- [x] Initial Research  
- [ ] Minimum viable product <-- You are Here  
- [ ] Alpha Release  
- [ ] Feature-Complete Release  

## Contributing

### Main Branch
Protected and can only be pushed to via pull requests. Should be considered stable and a representation of production code.

### Dev Branch
Should be considered fragile, code should compile and run but features may be prone to errors.

### Feature Branches
A branch per feature being worked on.

https://nvie.com/posts/a-successful-git-branching-model/

## Program Structure

```mermaid
    C4Context
      title GUI for DAQ recordings

```

## License

## Citation

Please cite the associated papers for this work if you use this code:

```
@article{xxx2023paper,
  title={Title},
  author={Author},
  journal={arXiv},
  year={2023}
}
```


## Acknowledgements
This work was funded by a grant from the UK Research Councils, EPSRC grant ref. EP/L012345/1, “Example project title, please update”.



