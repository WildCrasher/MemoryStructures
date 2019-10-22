#ifndef DATA_H
#define DATA_H
#include <string>
struct Data
{
	int key;
	std::string text;

	bool operator < (const Data& str) const
	{
		return (key < str.key);
	}
};

#endif