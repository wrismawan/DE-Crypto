#include <iostream>
#include <fstream>
#include <string>
#include <string.h>
#include <cstdlib>
using namespace std;
int main() {
    ofstream file_output;
    file_output.open("data_uji_4.txt");

    int A, B, CC, i;
    ifstream ifs("data4.txt");
    char plain[10000];
    string S;
    char plaintext[10000];
    i=0;
    
    while(getline(ifs,S)) {
        CC=S.length();
        for(int j=0;j<CC;j++){
            plain[i]=S[j];i++;
        }
    }
    
    int newI=0;
    for (int i=0;i<CC;i++){
        if (isalpha(plain[i])){
            plaintext[newI] = plain[i];
            newI++;
        }
    }
    
    cout<<plaintext<<endl;
    int C = strlen(plaintext);
    int D;
    
    cout << "Masukkan panjang kunci : " <<endl;
    cin >> D;
    
    int CA=D-(C%D);
    for(int i=0;i<CA;i++)
        plaintext[C+i]='a' + rand()%26;
    
    C=C+CA;

    int key[D];
    cout << "Masukkan kunci : " << endl;
    for (int i=0; i<D; i++){
        cin >> key[i];
        if (key[i]>D){
            cout<<"Masukkan kunci yang lain"<<endl;cin >> key[i];
        }

        for(int j=0;j<i;j++){
            if(key[i]==key[j]){
                cout<<"Masukkan kunci yang lain"<<endl;cin >> key[i];
            }
        }
    }

    file_output<<"====================================================="<<endl;
    file_output<<"SUMMARY"<<endl;
    file_output<<"====================================================="<<endl;
    file_output<<"PLAINTEXT : "<<endl;
    file_output<<plain<<endl;
    file_output<<"PANJANG PLAINTEXT : "<<newI<<endl;
    file_output<<"PANJANG KUNCI : "<<D<<endl;
    file_output<<"KUNCI : ";
    for(int i=0;i<D;i++)
        file_output<<key[i]<<" ";
    file_output<<endl;
    file_output<<"CIPHERTEXT : "<<endl;
    for (int i=0; i<C; i++){
        A = i%D;
        B = i/D;
        file_output<<plaintext[B*D+key[A]-1];
    }
    file_output<<endl;
    return 0;
}
