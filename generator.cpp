#include "data.h"
#include <vector>
#include <iostream>
#include <algorithm>
class Generator
{
private:
	int m_size;
public:
	std::vector <Data> randomSet;
	std::vector <Data> ascSet;


	Generator(int size)
	{
		m_size = size;
		generateRandom(size);
		generateAsc();
	}

	void generateAsc() {
		std::sort(ascSet.begin(), ascSet.end());
	}

	void generateRandom(int size)
	{
		for (int i = 0; i < size; i++) {
			struct Data c;
			c.key = rand();
			c.text = random_string(40);
			randomSet.push_back(c);
		}
		ascSet = randomSet;
	}

	std::string random_string(std::string::size_type length)
	{
		static auto& chrs = "0123456789"
			"abcdefghijklmnopqrstuvwxyz"
			"ABCDEFGHIJKLMNOPQRSTUVWXYZ";
		std::string s;
		s.reserve(length);
		while (length--)
			s += chrs[rand() % strlen(chrs)];

		return s;
	}

	int getSize() { return m_size; }
};

int main()
{
	int len = 10;
	Generator testSet(len);
	//for (int i = 0; i < len; i++) {
	//	std::cout << testSet.randomSet[i].key << "  " << testSet.randomSet[i].text << "\n";
	//}
	//for (int i = 0; i < len; i++) {
	//	std::cout << testSet.ascSet[i].key << "  " << testSet.ascSet[i].text << "\n";
	//}
	//getchar();
	return 0;
}